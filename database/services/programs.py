from database.models import Programs
from utils import current_time
from datetime import datetime

def upsert_program(program_name, scopes, ooscopes, config):
    program = Programs.objects(program_name=program_name).first()

    if program:
        program.config = config
        program.scopes = scopes
        program.ooscopes = ooscopes
        program.save()
        print(f"[{current_time()}] Updated program: {program.program_name}")
    else:
        new_program = Programs(
            program_name=program_name,
            created_date=datetime.now(),
            config=config,
            scopes=scopes,
            ooscopes=ooscopes
        )
        new_program.save()
        print(f"[{current_time()}] Inserted new program: {new_program.program_name}")
