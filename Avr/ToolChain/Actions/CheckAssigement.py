import sys, pathlib, traceback

p = pathlib.Path(__file__).resolve()

#these paths will be used in all actions
sys.path.append(r'C:\Users\rolfl\Documents\GIBZ\py')
print( p )
sys.path.append(str(p.parent.parent / "PyScripts"))


import StudentsInfo
import ExchangeHelpers
import CheckoutGitRepo

ProjectsRoot = r"e:\M242"
CurrentAssigement = "HelloWorld"
schuelerInfo = r"C:\Users\rolfl\OneDrive - GIBZ\M242\Semester2020\SchuelerInfo.xlsx"
schuelerRatings = r"C:\Users\rolfl\OneDrive - GIBZ\M242\Semester2020\M242_2020.pickle"

ratings = StudentsInfo.RatingCollection(schuelerInfo, schuelerRatings)
inaccessibleRepos = []
failingBuilds = []

def StudentFilter(x):
    return x.Student.NameToIdentifier() in ["Tillo_Beffa"   ]

def AssignementNotYetRated(x):
    return not x.HasAssignement(CurrentAssigement)

try:
    for studentRating in ratings.Filter(
        StudentFilter ):
        s = studentRating.Student
        print( "checking assignement of ", s.Name )
        try:
            print("try to get reop of", s.Name)
            CheckoutGitRepo.GitCloneOrUpdateRepo(ProjectsRoot, s.NameToIdentifier(), "M242", s.GithubRepo )
        except:
            print("failed to clone or Update repo of", s.Name)
            traceback.print_exc()
            inaccessibleRepos.append(s.Email)
            continue
        input("!!disconnect UART!!")
        try:
            CheckoutGitRepo.BuildProject(ProjectsRoot, s.NameToIdentifier(), CurrentAssigement)
        except:
            print("failed to build project")
            failingBuilds.append(s.Email)
            input("check assignement of {0}:".format(s.Name))
            continue
        passFail = input("Pass? =>p/f:")
        comment = input("Enter comment for assignement of {0}:".format(s.Name))
        studentRating.AddRating( StudentsInfo.Rating(CurrentAssigement, comment, passFail.find('p')!=-1))
finally:
    ratings.Save()
