import datetime
from mors_module.models import Program, Broadcast


class CurrentlyPlaying:
    """"
        Класс отвечает за функционал текщего воспроизведения
    """

    default_value = {
        "time": "до следующего эфира",
        "title": "просто музыка",
        "guests": ""
    }

    def now_playing(self):

        current_date = datetime.datetime.today()
        programs = Program.query.filter(Broadcast.date == current_date.strftime('%d.%m.%Y')).all()

        if len(programs) > 0:
            for item in programs:
                _temp = item.time.split(' - ')
                start_time = _temp[0].split(':')
                end_time = _temp[1].split(':')
                st_obj = current_date.replace(hour=int(start_time[0]), minute=int(start_time[1]))
                et_obj = current_date.replace(hour=int(end_time[0]), minute=int(end_time[1]))
                if st_obj < current_date < et_obj:
                    program = {
                        "time": item.time,
                        "title": item.title
                    }
                    break
            else:
                program = self.default_value
        else:
            program = self.default_value

        return program
