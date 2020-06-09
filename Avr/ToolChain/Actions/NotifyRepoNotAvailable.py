import sys, pathlib, traceback

p = pathlib.Path(__file__)

#these paths will be used in all actions
sys.path.append(r'C:\Users\rolfl\Documents\GIBZ\py')
sys.path.append(str(p.parent.parent / "PyScripts"))


import StudentsInfo
import ExchangeHelpers
import CheckoutGitRepo

ProjectsRoot = r"e:\M242"
schuelerInfo = r"C:\Users\rolfl\OneDrive - GIBZ\M242\Semester2020\SchuelerInfo.xlsx"

students = StudentsInfo.Open(schuelerInfo)

noGithubRepo ="""
Hallo,
Ich habe von ihnen noch keine Angaben zum Github-Repository erhalten. Die Angabe eines Git-Repositories ist
zwingend notwendig für die Abgabe der Übungen!
"""

failureAccessingGitRepo = """
Hallo,
Auf das von ihnen angegebene Repo konnte nicht zugegriffen werden.
Machen Sie das Repo public oder erteilen Sie mir Zugriffsrechte auf das Repo!
"""

missingRepos = list(map(lambda x: x.Email, students.Filter(lambda x: x.GithubRepo == None )))
inaccessibleRepos = []
for s in students.Filter(lambda x: x.GithubRepo != None):
    try:
        print("try to get reop of", s.Name)
        CheckoutGitRepo.GitCloneOrUpdateRepo(ProjectsRoot, s.NameToIdentifier(), "M242", s.GithubRepo )
    except:
        print("failed to clone or Update repo of", s.Name)
        traceback.print_exc()
        inaccessibleRepos.append(s.Email)

print( missingRepos )
print( inaccessibleRepos )

ExchangeHelpers.Send_Email("Fehlendes Git Repository!", missingRepos, noGithubRepo )
ExchangeHelpers.Send_Email("Zugriff auf Git Repository nicht möglich!", missingRepos, noGithubRepo )
