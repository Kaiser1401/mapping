import sys
import os
import csv

class pointFile:
    def __init__(self,path,group=""):
        self.group = group
        self.path=path

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (self.path)

class utmPoint:
    def __init__(self,x,y,z,group = ""):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.group = group

    def assign(self, other):
        self.x = other.x
        self.y = other.y
        self.z = other.z

    def min(self,other):
        self.x = min(self.x, other.x)
        self.y = min(self.y, other.y)
        self.z = min(self.z, other.z)

    def max(self,other):
        self.x = max(self.x, other.x)
        self.y = max(self.y, other.y)
        self.z = max(self.z, other.z)

    def __sub__(self, other):
        return utmPoint(self.x-other.x,self.y-other.y,self.z-other.z)

    def __add__(self, other):
        return utmPoint(self.x+other.x,self.y+other.y,self.z+other.z)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return ("%f %f %f" % (self.x, self.y, self.z))


class mainProgram:
    def __init__(self,arguments):
        self.arguments = arguments

    def passes_filter(self,point):
        if not self.doFilter:
            return True
        else:
            bValid = (point.x < self.xmax)
            bValid = (point.x > self.xmin) & bValid
            bValid = (point.y < self.ymax) & bValid
            bValid = (point.y > self.ymin) & bValid
            return bValid

    def main(self):
        if len(arguments) <= 0:
            print ("usage: %s path [x_min x_max y_min y_max]" % sys.argv[0])
            return

        folder = os.path.abspath(arguments[0])


        self.doFilter = len(arguments) >= 5

        if self.doFilter:
            self.xmin = float(arguments[1])
            self.xmax = float(arguments[2])
            self.ymin = float(arguments[3])
            self.ymax = float(arguments[4])


        filelist = []
        #bDoSeparateElements = True
        bDoSeparateElements = False

        elements = ["ab", "ag", "aw", "brk", "lpb", "lpnb", "lpub"]

        if self.doFilter:

            # dgm1l-ab_32357_5757_1_nw.xyz

            prefix = "dgm1l"
            zone = 32
            resoultion = 1  # kms
            postfix = "_nw.xyz"

            print ("creating filtered filelist in %s " % folder)
            minfx = int(self.xmin // (resoultion * 1000)) * resoultion
            maxfx = int(self.xmax // (resoultion * 1000)) * resoultion
            minfy = int(self.ymin // (resoultion * 1000)) * resoultion
            maxfy = int(self.ymax // (resoultion * 1000)) * resoultion

            for e in elements:
                for x in range(minfx,maxfx+1,resoultion):
                    for y in range(minfy, maxfy + 1, resoultion):
                        fn = ("%s-%s_%d%d_%d_%d%s" % (prefix,e,zone,x,y,resoultion,postfix))
                        filelist.append(pointFile(os.path.join(folder, fn),e))

            #print(filelist)
            #return

        else:
            print ("scanning %s for .xyz files ..." % folder)


            for file in os.listdir(folder):
                if file.endswith(".xyz"):
                    filelist.append(os.path.join(folder, file))

        filecount = len(filelist)
        print ("trying to scan %d files" % filecount)



        pointList = []

        minPoint = utmPoint(0, 0, 0)
        maxPoint = utmPoint(0, 0, 0)

        bNotFirst = False
        n = 1

        for file in filelist:
            print ("processing file %d/%d" % (n,filecount))
            n+=1
            try:
                with open(file.path) as csvfile:
                    reader = csv.DictReader(csvfile,["x","y","z"])
                    for row in reader:
                        try:
                            aPoint = utmPoint(row["x"],row["y"],row["z"],file.group)
                            if self.passes_filter(aPoint):
                                if bNotFirst:
                                    minPoint.min(aPoint)
                                    maxPoint.max(aPoint)
                                else:
                                    minPoint.assign(aPoint)
                                    maxPoint.assign(aPoint)
                                    bNotFirst = True

                                pointList.append(aPoint)
                        except:
                            print ("Error in %s row: %s" % (file, str(row)))
            except:
                print ("Error opening file: %s" % (file))

        print("selected %d points" % len(pointList))

        print("setting origin to %s" % str(minPoint))


        outfiles = dict()
        group = "combined"

        folder = os.path.join(folder,"output")
        try:
            os.mkdir(folder)
        except:
            pass

        if bDoSeparateElements:
            for e in elements:
                outfilename = ("out_xyz_spaced_%s.xyz" % e)
                outfiles[e] = os.path.join(folder, outfilename)
        else:
            outfilename = ("out_xyz_spaced_%s.xyz" % group)
            outfiles[group] = os.path.join(folder, outfilename)

        outfilehandles = dict()
        for file in outfiles:
            try:
                os.remove(outfiles[file])
            except:
                pass
            try:
                outfilehandles[file] = open(outfiles[file], "a")
            except:
                pass

        #with open(outfile, "a") as f:
#            for point in pointList:
#                f.write('%s \n' % str(point-minPoint))

        #print(outfiles)

        for point in pointList:
            if bDoSeparateElements:
                outfilehandles[point.group].write('%s \n' % str(point - minPoint))
            else:
                outfilehandles[group].write('%s \n' % str(point-minPoint))

        # f.write('%s \n' % str(point-minPoint))

        print("saved selected points to:")
        for file in outfiles:
            print(outfiles[file])




if __name__ == "__main__":
    arguments = sys.argv[1:]
    prog = mainProgram(arguments)
    prog.main()
