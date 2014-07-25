import os
import jpype


if jpype.isJVMStarted()!= True:
    jars=[]
    for top,dirs,files in os.walk('./'):
        for filename in files:
            if filename[-4:]=='.jar':
                jars.append(os.path.join(top,filename))
    jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=%s" % os.pathsep.join(jars))
