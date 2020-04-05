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

        current_datetime = datetime.datetime.today()
        current_date = datetime.datetime(current_datetime.year, current_datetime.month, current_datetime.day)
        broadcasts = Broadcast.query.all()
        bcast_id = None
        for broadcast in broadcasts:
            if broadcast.date == current_date:
                bcast_id = broadcast.id
        if bcast_id:
            programs = Program.query.filter(Program.broadcast_id == bcast_id).all()
            for item in programs:
                _temp = item.time.split(' - ')
                start_time = _temp[0].split(':')
                end_time = _temp[1].split(':')
                st_obj = current_datetime.replace(hour=int(start_time[0]), minute=int(start_time[1]))
                et_obj = current_datetime.replace(hour=int(end_time[0]), minute=int(end_time[1]))
                if st_obj < current_datetime < et_obj:
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
