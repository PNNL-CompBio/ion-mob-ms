# This script reads all Agilent .d files in a directory
# extract metadata from xml files (e.g., acquisition time)
# generates a single csv with the metadata of all .d files found.
# Author: Bilbao Pena, Aivett <aivett.bilbao@pnnl.gov>

ExtractAgilentdFileMetadata = function(input,
                                       outputFile)
{
  inputFiles = NULL
  if(grepl(".txt$", input))
  {
    inputFiles = readLines(input)
  }else{
    # Load all files in directory  
    myPattern = ".+\\.d$"
    inputFiles = list.dirs(path = input, full.names = TRUE, recursive = TRUE)
    inputFiles = inputFiles[grepl(myPattern, inputFiles)]
  }
  
  dat = data.frame(RawFileName = inputFiles)
  # ----------------------------------------
  # Instrument metadata:
  
  # Get AcquiredTime, Instrument and ion polarity for each file:
  contentsFile = "AcqData/Contents.xml"
  dat$AcquiredTime = ""
  dat$InstrumentName = ""
  # e.g.  <AcquiredTime>2018-09-26T15:18:59Z</AcquiredTime>
  for(i in 1:length(dat[,1]))
  {
    fileName = file.path(dat$RawFileName[i], contentsFile)
    txt = readChar(fileName, file.info(fileName)$size)
    dat$AcquiredTime[i] = sub(".+<AcquiredTime>(.+)</AcquiredTime>.+", "\\1", txt)
    dat$InstrumentName[i] = sub(".+<InstrumentName>(.+)</InstrumentName>.+", "\\1", txt)
  }
  dat$AcquiredTime = gsub("-|:",'', dat$AcquiredTime)
  dat$AcquiredTime = substring(dat$AcquiredTime, 1, 15)
  
  # Acquisition dates across all runs
  #print(unique(substring(dat$AcquiredTime, 1,8)))
  
  imsFrameMethodFile = "AcqData/IMSFrameMeth.xml"
  dat$IonPolarity = ""  
  # e.g.     <!--0=Pos; 1=Neg; 3=Mixed-->
  #          <IonPolarity>0</IonPolarity>
  for(i in 1:length(dat[,1]))
  {
    fileName = file.path(dat$RawFileName[i], imsFrameMethodFile)
    txt = readChar(fileName, file.info(fileName)$size)
    dat$IonPolarity[i] = sub(".+<IonPolarity>(.+)</IonPolarity>.+", "\\1", txt)
  }
  dat$IonPolarity[grepl("0", dat$IonPolarity)] = "POS"
  dat$IonPolarity[grepl("1", dat$IonPolarity)] = "NEG"
  dat$IonPolarity[grepl("3", dat$IonPolarity)] = "MIX"
  
  # Get PLate and Well position AcquiredTime and ion polarity for each file:
  sampleInfoFile = "AcqData/sample_info.xml"
  dat$Well = ""
  dat$Cartridge = ""
  # 
  # <Name>Plate Position</Name>
  #  <DisplayName>Plate Position</DisplayName>
  #  <Value>MAT2</Value>
  for(i in 1:length(dat[,1]))
  {
    fileName = file.path(dat$RawFileName[i], sampleInfoFile)
    txt = readChar(fileName, file.info(fileName)$size)
    dat$Well[i] = sub(".+<DisplayName>Plate Position</DisplayName>[[:space:]]+<Value>([A-Z]+[0-9]+)</Value>.+", "\\1", txt)
    dat$Well[grep("<SampleInfo>", dat$Well)] = ""
    if(grepl("Graphitic Carbon", txt))
      dat$Cartridge[i] = "GC"
    if(grepl("C18", txt))
      dat$Cartridge[i] = "C18"
    if(grepl("HILIC", txt))
      dat$Cartridge[i] = "HILIC"
  }
  
  dat$RawFileName = basename(dat$RawFileName)
  dat$RawFileName = sub("\\.d$", "", dat$RawFileName)
  # Save file mapping names and metadata
  write.csv(dat, file = outputFile, row.names = FALSE)

  return(TRUE)
}
