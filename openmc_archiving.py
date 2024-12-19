import os
import shutil
import datetime
import json
from lxml import etree
import lxml.builder

# create an archive "run_date_time" in the current calculation directory
# should the script file itself be saved ?

# INPUT : none
# OUTPUT : a new folder "run_date_time"
def createArchiveDirectory():
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y%m%d_%H%M%S")
    datafolder="./run_"+formatted_date+"/"
    os.mkdir(datafolder)
    return .pydatafolder

# INPUT : the archive directory (as create by the above procedure) + a file to archive
# OUTPUT : the file is moved in the new directory
# TO DO : error processing especially checking the file to be saved exists
def archiveFile(archdir,myFile):
    if os.path.exists(myFile):
        os.rename(myFile, archdir+myFile)
    else:
        print("The file "+myFile+" does not exist")

# INPUT : the archive directory (as create by the above procedure) + the sp_filename
#         the other files are saved with their default name model.xml, summary.h5, surface_source.h5
#         the script actually used for the simulation
# OUTPUT : the files are moved in the archive directory
#          a <configuration.xml> file is created
def createArchivedDatasetXML(archDir, # COMPULSORY, NEEDS TO BE SPECIFIED
                              statepoint = "not specified", 
                              script = "not specified",  
                              surfaceSource='surface_source.h5',
                              comment = "MyComment", source = "not specified", geometry = "not specified"):
    myFile='model.xml'
    archiveFile(archDir, myFile)
    myFile='summary.h5'
    archiveFile(archDir, myFile)
    myFile=surfaceSource
    archiveFile(archDir, myFile)
    a=str(statepoint);myFile=a.rsplit('/',1)[1]
    archiveFile(archDir, myFile)
    # saving the script
    shutil.copy(script, archdir+script)
    
    # add the creation of a <configuration.xml> file
    E=lxml.builder.ElementMaker() 
    root = E.configuration(
        E.comments(comment),
        E.files(
            E.script(script),  # defaultValue
            E.surfaceWrite(surfaceSource),  # define explicitley as the defaultValue
            E.statePoint(str(sp_filename))
        ),
        E.source(
            E.model(source), # correspodign to the source used in <source_ICONE>
            # E.parameters('27')
            ),
        E.geometry(
            E.model(geometry),
            #E.parameters(
             #   E.e0('27')
            )
        )
    # Convertir l'élément racine en une chaîne XML
    xml_string = etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')
    # Écrire le contenu dans un fichier
    with open(archdir+'configuration.xml', 'wb') as f:
        f.write(xml_string.encode('utf-8'))
        
# INPUT : the archive directory (as create by the above procedure) + the sp_filename
#         the other files are saved with their default name model.xml, summary.h5, surface_source.h5
#         the script actually used for the simulation
#         the source model used for the simulations and the corresponding parameters (input as a dictionnary)
#         the geometry model used for the simulations and the corresponding parameters (input as a dictionnary)
# OUTPUT : the files are moved in the archive directory
#          a <configuration.json> file is created
def createArchivedDataset(archDir, # COMPULSORY
                          statepoint = "not specified", 
                          script = "not specified",  
                          surfaceSource='surface_source.h5',
                          comment = "MyComment", 
                          source = "not specified", sourcePara = { },
                          geometry = "not specified", geometryPara = { }):
    myFile='model.xml'
    archiveFile(archDir, myFile)
    myFile='summary.h5'
    archiveFile(archDir, myFile)
    myFile=surfaceSource
    archiveFile(archDir, myFile)
    a=str(statepoint);statepoint_str=a.rsplit('/',1)[1]
    archiveFile(archDir, statepoint_str)
    # saving the script
    shutil.copy(script, archDir+script)
    
    # add the creation of a <configuration.json> file
    # configuration = { 'script': script, 'surfaceWrite':surfaceSource, 'statePoint': statepoint_str,
                   # 'source':source, 'geometry':geometry} 
    configuration = { 'comment': comment,
                     'files': {'script': script, 'surfaceWrite':surfaceSource, 'statePoint': statepoint_str },
                     'source':{ 'sourceName':source,'sourceParameters':sourcePara }, 
                     'geometry': { 'geometryName':geometry, 'geometryParameters':geometryPara}
                    } 
    # print(configuration)
    
    with open('configuration.json','w') as f:
        json.dump(configuration,f)
        archiveFile(archDir, 'configuration.json')
         
        
# EXAMPLE
# from openmc_archiving import *
# archDir=createArchiveDirectory() # this creates a new folder "./run_date_time" in the working script directory
# createArchivedDataset(archDir,statepoint=sp_filename, script="modules_testing_V1.ipynb",
#                       comment="essai n°3", source="Neutron 25MeV", geometry="Baseline_V1", geometryPara={'e0':26} 
                          
        
