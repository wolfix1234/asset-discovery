from database.models import Programs


def get_all_programs():
    return Programs.objects().all()


def delete_prg(program_name):
    return Programs.objects(program_name=program_name).delete()


def get_program_by_scope(domain):
    return Programs.objects(scopes=domain).first()
