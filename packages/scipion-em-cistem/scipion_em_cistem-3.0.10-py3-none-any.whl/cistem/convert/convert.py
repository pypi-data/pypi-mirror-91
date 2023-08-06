# **************************************************************************
# *
# * Authors:     Josue Gomez Blanco (josue.gomez-blanco@mcgill.ca) [1]
# *
# * [1] Department of Anatomy and Cell Biology, McGill University
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import os
import numpy as np
from collections import OrderedDict
from pwem.objects import (Coordinate, SetOfClasses2D, SetOfAverages,
                          Transform, CTFModel)
from pwem.constants import ALIGN_PROJ
from pwem.emlib.image import ImageHandler
import pwem.convert.transformations as transformations
from pyworkflow.utils import replaceBaseExt, join, exists


HEADER_COLUMNS = ['INDEX', 'PSI', 'THETA', 'PHI', 'SHX', 'SHY', 'MAG',
                  'FILM', 'DF1', 'DF2', 'ANGAST', 'PSHIFT', 'OCC',
                  'LogP', 'SIGMA', 'SCORE', 'CHANGE']


class FrealignParFile(object):
    """ Handler class to read/write frealign metadata."""
    def __init__(self, filename, mode='r'):
        self._file = open(filename, mode)
        self._count = 0

    def __iter__(self):
        for line in self._file:
            line = line.strip()
            if not line.startswith('C'):
                row = OrderedDict(zip(HEADER_COLUMNS, line.split()))
                yield row

    def close(self):
        self._file.close()


def readSetOfParticles(inputSet, outputSet, parFileName):
    """
     Iterate through the inputSet and the parFile lines
     and populate the outputSet with the same particles
     of inputSet, but with the angles and shift (3d alignment)
     updated from the parFile info.
     It is assumed that the order of iteration of the particles
     and the lines match and have the same number.
    """
    # create dictionary that matches input particles with param file
    samplingRate = inputSet.getSamplingRate()
    parFile = FrealignParFile(parFileName)
    partIter = iter(inputSet.iterItems(orderBy=['_micId', 'id'], direction='ASC'))

    for particle, row in zip(partIter, parFile):
        particle.setTransform(rowToAlignment(row, samplingRate))
        # We assume that each particle have ctfModel
        # in order to be processed in Frealign
        # JMRT: Since the CTF will be set, we can setup
        # an empty CTFModel object
        if not particle.hasCTF():
            particle.setCTF(CTFModel())
        rowToCtfModel(row, particle.getCTF())
        outputSet.append(particle)
    outputSet.setAlignment(ALIGN_PROJ)


def rowToCtfModel(ctfRow, ctfModel):
    defocusU = float(ctfRow.get('DF1'))
    defocusV = float(ctfRow.get('DF2'))
    defocusAngle = float(ctfRow.get('ANGAST'))
    ctfModel.setStandardDefocus(defocusU, defocusV, defocusAngle)


def parseCtffind4Output(filename):
    """ Retrieve defocus U, V and angle from the
    output file of the ctffind4 execution.
    """
    result = None
    if os.path.exists(filename):
        with open(filename) as f:
            for line in f:
                if not line.startswith("#"):
                    result = tuple(map(float, line.split()[1:7]))
                    break
    else:
        print("Warning: Missing file: ", filename)
    return result


def setWrongDefocus(ctfModel):
    ctfModel.setDefocusU(-999)
    ctfModel.setDefocusV(-1)
    ctfModel.setDefocusAngle(-999)
    
    
def readCtfModel(ctfModel, filename):
    result = parseCtffind4Output(filename)
    if result is None:
        setWrongDefocus(ctfModel)
        ctfFit, ctfResolution, ctfPhaseShift = -999, -999, 0
    else:
        defocusU, defocusV, defocusAngle, ctfPhaseShift, ctfFit, ctfResolution = result
        ctfModel.setStandardDefocus(defocusU, defocusV, defocusAngle)
    ctfModel.setFitQuality(ctfFit)
    ctfModel.setResolution(ctfResolution)

    # Avoid creation of phaseShift
    ctfPhaseShiftDeg = np.rad2deg(ctfPhaseShift)
    if ctfPhaseShiftDeg != 0:
        ctfModel.setPhaseShift(ctfPhaseShiftDeg)


def readShiftsMovieAlignment(shiftFn):
    with open(shiftFn, 'r') as f:
        xshifts = []
        yshifts = []

        for line in f:
            line2 = line.strip()
            if line2.startswith('image #'):
                parts = line2.split()
                xshifts.append(float(parts[-2].rstrip(',')))
                yshifts.append(float(parts[-1]))
    return xshifts, yshifts


def writeShiftsMovieAlignment(movie, shiftsFn, s0, sN):
    movieAlignment = movie.getAlignment()
    shiftListX, shiftListY = movieAlignment.getShifts()

    # Generating metadata for global shifts
    a0, aN = movieAlignment.getRange()
    alFrame = a0

    if s0 < a0:
        diff = a0 - s0
        initShifts = "0.0000 " * diff
    else:
        initShifts = ""

    if sN > aN:
        diff = sN - aN
        finalShifts = "0.0000 " * diff
    else:
        finalShifts = ""

    shiftsX = ""
    shiftsY = ""
    for shiftX, shiftY in zip(shiftListX, shiftListY):
        if s0 <= alFrame <= sN:
            shiftsX = shiftsX + "%0.4f " % shiftX
            shiftsY = shiftsY + "%0.4f " % shiftY
        alFrame += 1

    with open(shiftsFn, 'w') as f:
        shifts = (initShifts + shiftsX + " " + finalShifts + "\n"
                  + initShifts + shiftsY + " " + finalShifts)
        f.write(shifts)


def readSetOfCoordinates(workDir, micSet, coordSet):
    """ Read from cisTEM .plt files. """
    for mic in micSet:
        micCoordFn = join(workDir, replaceBaseExt(mic.getFileName(), 'plt'))
        readCoordinates(mic, micCoordFn, coordSet)


def readCoordinates(mic, fn, coordsSet):
    if exists(fn):
        with open(fn, 'r') as f:
            for line in f:
                values = line.strip().split()
                # plt coords are in Imagic style
                x = float(values[1])
                y = float(mic.getYDim() - float(values[0]))
                coord = Coordinate()
                coord.setPosition(x, y)
                coord.setMicrograph(mic)
                coordsSet.append(coord)


def writeReferences(inputSet, outputFn):
    """
    Write references star and stack files from SetOfAverages or SetOfClasses2D.
    Params:
        inputSet: the input SetOfParticles to be converted
        outputFn: where to write the output files.
    """
    ih = ImageHandler()

    def _convert(item, n):
        index = n + 1
        ih.convert(item, (index, outputFn))
        item.setLocation(index, outputFn)

    if isinstance(inputSet, SetOfAverages):
        for i, img in enumerate(inputSet):
            _convert(img, i)
    elif isinstance(inputSet, SetOfClasses2D):
        for i, rep in enumerate(inputSet.iterRepresentatives()):
            _convert(rep, i)
    else:
        raise Exception('Invalid object type: %s' % type(inputSet))


def rowToAlignment(alignmentRow, samplingRate):
    """
    Return an Transform object representing the Alignment
    from a given parFile row.
    """
    angles = np.zeros(3)
    shifts = np.zeros(3)
    alignment = Transform()
    # PSI   THETA     PHI       SHX       SHY
    angles[0] = float(alignmentRow.get('PSI'))
    angles[1] = float(alignmentRow.get('THETA'))
    angles[2] = float(alignmentRow.get('PHI'))
    shifts[0] = float(alignmentRow.get('SHX')) / samplingRate
    shifts[1] = float(alignmentRow.get('SHY')) / samplingRate

    M = matrixFromGeometry(shifts, angles)
    alignment.setMatrix(M)

    return alignment


def matrixFromGeometry(shifts, angles):
    """ Create the transformation matrix from a given
    2D shifts in X and Y...and the 3 euler angles.
    """
    radAngles = -np.deg2rad(angles)

    M = transformations.euler_matrix(
        radAngles[0], radAngles[1], radAngles[2], 'szyz')
    M[:3, 3] = -shifts[:3]
    M = np.linalg.inv(M)

    return M


def geometryFromMatrix(matrix):
    matrix = np.linalg.inv(matrix)
    shifts = -transformations.translation_from_matrix(matrix)
    angles = -np.rad2deg(transformations.euler_from_matrix(matrix, axes='szyz'))

    return shifts, angles
