from main.models import Group, GroupStudent, User


def main(request):
    total_teachers = User.objects.filter(ut=2).count()
    total_groups = Group.objects.all().count()
    return {
        "total_teachers": total_teachers,
        "total_groups": total_groups,
    }




