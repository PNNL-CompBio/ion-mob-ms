# This script reads all .csv feature files in a directory
# and a list of target ions (adducts with m/z),
# matches by m/z and tolerance (and CCS if expected value is provided),
# and generates a single csv with all annotated features found.
# Author: Bilbao, Aivett <aivett.bilbao@pnnl.gov>

AnnotateCalibratedFeatures = function(pathToCalibratedFeatures,
                                      rawFilesMetadata,
                                      targetListIons,
                                      outputFolder,
                                      mzTolerancePpm)
{

  TLI = list.files(targetListIons,pattern="*.csv")
  TLI = paste(targetListIons,"/",TLI,sep="")
  RFM = list.files(rawFilesMetadata,pattern="*.csv")
  RFM = paste(rawFilesMetadata,"/",RFM,sep="")
  print("TLI IS")
  print(TLI)
  print("RMF IS")
  print(RFM)
  targets = read.csv(file = TLI[1], stringsAsFactors = FALSE)
  rawfilesmeta = read.csv(file = RFM, stringsAsFactors = FALSE)
  
  featureFiles = list.files(path = pathToCalibratedFeatures, full.names = FALSE, pattern = ".+\\.mzML.+\\.csv$")
  
  targets$Ionization = toupper(targets$Ionization)
  rawfilesmeta$IonPolarity = toupper(rawfilesmeta$IonPolarity)
  
  dat = NULL
  notFound = NULL
  for(k in 1:length(targets[,1]))
  {
    # find the feature files corresponding to the target:
    kfeatFile = featureFiles[grepl(paste(targets$UniqueID4RawFileNames[k], "[_|\\-]", sep = ''), featureFiles)]
    
    for(f in kfeatFile)
    {
      indexMeta = which(rawfilesmeta$RawFileName == sub("\\.mzML.*", "",f))
      if(targets$Ionization[k] != rawfilesmeta$IonPolarity[indexMeta]) # skip if ionization mode does not match
        next
      
      tb = read.csv(file = file.path(pathToCalibratedFeatures, f), stringsAsFactors = FALSE, sep = ',')
      colnames(tb) = sub("(.+\\.mzML.)", "", colnames(tb)) # remove file name prefix from column names
      colnames(tb) = sub(paste(f,""), "", colnames(tb))
      
      tb$mz_difference_ppm = (tb$Peak.m.z - targets$Adduct_mz[k]) / targets$Adduct_mz[k] * 1E6
      tb = tb[which(abs(tb$mz_difference_ppm) < mzTolerancePpm),]
      if(length(tb[,1]) > 0)
      {
        tb$RawFileName = rawfilesmeta$RawFileName[indexMeta]
        tb = cbind(targets[k,], tb, row.names = NULL)
        dat = rbind(dat, tb)
      }else{
        notFound = rbind(notFound, targets[k,])
      }
    }
  }

  # Write a single output table with all features found:
  if(nrow(dat) > 0)
  {
    dat$ccs_difference_percent = (dat$calibrated_ccs - dat$ExpectedCCS)/dat$ExpectedCCS*100
  
    write.table(dat, file.path(outputFolder,"ccs-table_Features-Annotated.csv"),
              col.names = TRUE, row.names = FALSE, sep = ",")
  }
  
  if(nrow(notFound) > 0)
  {
    write.table(notFound, file.path(outputFolder,"ccs-table_targets-not-found.csv"),
                col.names = TRUE, row.names = FALSE, sep = ",")
  }
}


#Added as an optional step to end of autoCCS_step
#works for single field and SLIM

AnnotateCalibratedFeatures("/tmp/IV_Results","/tmp/MD","/tmp/TLF","/tmp/IV_Results",50)                            
