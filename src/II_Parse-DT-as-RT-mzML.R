# This script reads all .mzML files in a directory
# find and replace some XML tags to set the DT as RT, to be able to use MZmine feature finder.
# Author: Bilbao Pena, Aivett <aivett.bilbao@pnnl.gov>
# maintainer: Anubhav, Fnu <anubhav@pnnl.gov>

ParseDTasRTmzML = function(nCores,
                            pathTomzML)
{

  # Installing and loading packages:
  if(!"doParallel" %in% installed.packages())
    install.packages("doParallel")
  library("doParallel") # this paralellization package is used because it works for Windows and Unix-like systems

  # Load all files in directory
  myPattern = ".+\\.mzML$"
  allRawFiles = list.files(path = pathTomzML, full.names = FALSE, recursive = TRUE)
  allRawFiles = allRawFiles[grepl(myPattern, allRawFiles)]

  if(length(allRawFiles) == 0)
  {
    print("Error: No mzML files to process.")
    return(FALSE)
  }

  nCores = min(nCores, length(allRawFiles))
  workers = makeCluster(nCores)
  registerDoParallel(workers)
  foreach(f=allRawFiles, .options.snow=list(preschedule=TRUE)) %dopar%
  {
    # Change DT to RT in mzML:
    inputFile = file.path(pathTomzML, f)
    newFile = paste(inputFile, 'new', sep='')

    conn  <- file(inputFile, open = "r")
    connNew  <- file(newFile, open = "w")

    while (length(textLine <- readLines(conn, n = 1)) > 0)
    {
      # <cvParam cvRef="MS" accession="MS:1000016" name="scan start time" value="0.458416666667" unitCvRef="UO" unitAccession="UO:0000031" unitName="minute"/>
      # <cvParam cvRef="MS" accession="MS:1002476" name="ion mobility drift time" value="52.59584" unitCvRef="UO" unitAccession="UO:0000028" unitName="millisecond"/>
      if(grepl('name="scan start time"',textLine))
        next

      if(grepl('name="ion mobility drift time"',textLine))
      {
        originalText = textLine
        textLine = gsub("MS:1002476", "MS:1000016", textLine)
        textLine = gsub("ion mobility drift time","scan start time", textLine)
        textLine = gsub("UO:0000028", "UO:0000031", textLine)
        textLine = gsub('unitName="millisecond', 'unitName="minute', textLine)
        writeLines(originalText, connNew) # Keep original ion mobility element
      }
      writeLines(textLine, connNew)
    }

    close(conn)
    close(connNew)

    file.remove(inputFile)
    file.rename(newFile, inputFile)
  }
  stopCluster(workers) #close parallel backend

  return(TRUE)
}