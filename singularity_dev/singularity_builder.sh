#! /bin/bash

module load singularity
module load python/3.7.0


if [ -d "./proteowizard.sandbox" ] 
then
    echo "proteowizard.sandbox exists." 
else
    echo "proteowizard.sandbox does not exist. Attempting to build."
    singularity build --sandbox proteowizard.sandbox proteowizard.def
fi


if [ -f "mzmine.sif" ]
then
    echo "mzmine.sif exists."
else
    echo "mzmine.sif does not exist. Attempting to build."
    singularity build --fakeroot mzmine.sif mzmine.def
fi

if [ -f "autoccs.sif" ]
then
    echo "autoccs.sif exists."
else
    echo "autoccs.sif does not exist. Attempting to build."
    singularity build --fakeroot autoccs.sif autoccs.def
fi

