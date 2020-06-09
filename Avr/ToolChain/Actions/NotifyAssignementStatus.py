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
successfulCompletionBody ="""Congrats,
You successfully completed your assignement!
Comment from review: {0}
"""

for studentRating in ratings.Filter(lambda x: x.HasPassedAssignement(CurrentAssigement)
    and not x.GetAssignementRating(CurrentAssigement).IsNotified()):
    #ExchangeHelpers.Send_Email("Assignement {0} successfully completed".format(CurrentAssigement),
    #    [studentRating.Student.Email], successfulCompletionBody.format(
    #    studentRating.GetAssignementRating(CurrentAssigement).Comment))
    print( studentRating.Student.Name,
        studentRating.Student.Email,
        studentRating.GetAssignementRating(CurrentAssigement).Passed,
        studentRating.GetAssignementRating(CurrentAssigement).Comment )
    studentRating.GetAssignementRating(CurrentAssigement).SetNotified()
ratings.Save()
