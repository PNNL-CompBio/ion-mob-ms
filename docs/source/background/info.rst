Ion Mobility Dashboard
================================

The Ion Mobility Dashboard is designed to allow scientists to
generate results from PreProcessed Ion Mobility-Mass Spectrometry data without
requiring assistance from an engineer or bioinformatician. This
dashboard links several sequential command line tools into a single
user-friendly application which communicates with Docker Desktop to
dynamically spin up docker containers and manage the filesystem. Each
tool has been dockerized and together they perform the following steps:
quality control data processing, file type conversion (from proprietary
to an open-source format), detection of unique features, and calculation
of collision-cross section (CCS). Numerous intermediate shell scripts are also integrated into this pipeline.

IMS-MS Background
-----------------

Mass Spectrometry (MS) is used to identify and differentiate unknown
molecules by comparing intensities and mass-to-charge-ratio (m/z). This
is important in clinical research and drug development, however, this
method stuggles with identifying small molecules, isomers, and
enantiomers. To increase the accuracy of molecular identification, MS
can be paired with Ion Mobility Spectrometry (IMS). IMS generates an
additional descriptive variable called the “collision cross section”, or
CCS, which is used to further differentiate between unknown molecules.

| This application analyzes the following three methods of ion mobility
  spectrometry:
| 1) Single Field Drift Tube Ion Mobility Spectrometry (single field
  DTIMS)
| 2) Stepped Field Drift Tube Ion Mobility Spectrometry (stepped field
  DTIMS)
| 3) Structures for Lossless Ion Manipulations (SLIM)  
   
|      
**Drift Tube Ion Mobility Spectrometry**  
  
DTIMS seperates ions by collision cross section. This works by
accelerating ions through a straight tube filled with an inert buffer
gas, as the ions pass through the tube, they bump into buffer gas
molecules and are slowed down. Drift (retention) time is used as a
predictor of CCS. Ions with a greater CCS collide with and are slowed
down more by buffer molecules, the inverse is true with small molecules.
Single field DTIMS uses a single electrical field to accelerate ions
through the tube. This differs from stepped field DTIMS which uses an
alternating electrical curent to propel ions though the tube. An
increase in the length of drift tube increases resolution and both
methods of DTIMS are limited by instrument space.

**Structures for Lossless Ion Manipulations**

SLIM uses the same principal as single field DTIMS without the
limitation of drift tube length. This technology allows the ions to be
pushed around corners without colliding with path walls; this allows for
significantly longer paths resulting in much greater resolution of ion
CCS values.
