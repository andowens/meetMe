from agenda import *
import io

def selftest_appt():
    """Simple smoke test for Appt class."""
    earlier = Appt.from_string("10/31/2012 2:30 PM to 10/31/2012 3:45 PM| Before my appt")
    later = Appt.from_string("10/31/2012 4:00 PM to 10/31/2012 9:00 PM| Long dinner")
    assert earlier < later
    assert later > earlier
    assert not (earlier < earlier)
    assert not (earlier > later)

    assert not (earlier.overlaps(later))
    assert not (later.overlaps(earlier))

    conflict = Appt.from_string("10/31/2012 1:45 PM to 10/31/2012 4:00 PM| Conflicting appt")
    sample = Appt.from_string("10/31/2012 2:30 PM to 10/31/2012 3:45 PM| Sample appointment")
    assert sample.overlaps(conflict)
    assert conflict.overlaps(sample)
    overlap = sample.intersect(conflict)
    assert str(overlap) == "10/31/2012 2:30 PM to 10/31/2012 3:45 PM| Sample appointment"


def selftest_agenda():
    """#Simple smoke test for Agenda class."""

    keiko_agtxt="""# Free times for Keiko on December 1
           12/01/2012 7:00 AM to 12/01/2012 8:00 AM| Possible breakfast meeting
           12/01/2012 10:00 AM to 12/01/2012 12:00 PM| Late morning meeting
           12/01/2012 2:00 PM to 12/01/2012 6:00 PM| Afternoon meeting
         """

    kevin_agtxt="""
          11/30/2012 9:00 AM to 11/30/2012 2:00 PM| I have an afternoon commitment on the 30th
          12/01/2012 9:00 AM to 12/01/2012 3:00 PM| I prefer morning meetings
          # Kevin always prefers morning, but can be available till 3, except for
          # 30th of November.
          """

    emanuela_agtxt = """
    12/01/2012 12:00 PM to 12/01/2012 2:00 PM| Early afternoon
    12/01/2012 4:00 PM to 12/01/2012 6:00 PM| Late afternoon into evening
    12/02/2012 8:00 AM to 12/02/2012 5:00 PM| All the next day
    """

    keiko_ag = Agenda.from_file(io.StringIO(keiko_agtxt))
    kevin_ag = Agenda.from_file(io.StringIO(kevin_agtxt))
    emanuela_ag = Agenda.from_file(io.StringIO(emanuela_agtxt))

    kevin_emanuela = kevin_ag.intersect(emanuela_ag)
    ke = "12/01/2012 12:00 PM to 12/01/2012 2:00| I prefer morning meetings"
    keactual = str(kevin_emanuela)
    assert keactual == ke

    everyone = kevin_emanuela.intersect(keiko_ag)
    assert len(everyone) == 0

def selftest2_agenda():


    """Additional tests for agenda normalization and complement."""
    # What could go wrong in sorting?
    keiko_agtxt="""12/2/2013 12:00 PM to 12/2/2013 2:00 PM| Late lunch
                   12/1/2013 1:00 PM to 12/1/2013 2:00 PM| Sunday brunch
                   12/2/2013 08:00 AM to 3:00 PM| Long long meeting
                   12/2/2013 3:00 PM to 12/2/2013 4:00 PM| Coffee after the meeting"""
    keiko_ag = Agenda.from_file(io.StringIO(keiko_agtxt))

    # Torture test for normalization
    day_in_life_agtxt = """
    # A torture-test agenda.  I am seeing a lot of code
    # that may not work well with sequences of three or more
    # appointments that need to be merged.  Here's an agenda
    # with such a sequence.  Also some Beatles lyrics that have
    # been running through my head.
    #
    11/26/2013 9:00 AM to 11/26/2013 10:30 AM| got up
    11/26/2013 10:00 AM to 11/26/2013 11:30 AM| got out of bed
    11/26/2013 11:00 AM to 11/26/2013 12:30 PM| drug a comb across my head
    11/26/2013 12:00 PM to 11/26/2013 1:30 PM| on the way down stairs I had a smoke
    11/26/2013 1:00 PM to 11/26/2013 2:30 PM| and somebody spoke
    11/26/2013 2:00 PM to 11/26/2013 3:30 PM| and I went into a dream
    #
    # A gap here, from 15:30 to 17:00
    #
    11/26/2013 5:00 PM to 11/26/2013 6:30 PM| he blew his mind out in a car
    11/26/2013 6:00 PM to 11/26/2013 7:30 PM| hadn't noticed that the lights had changed
    11/26/2013 7:00 PM to 11/26/2013 8:30 PM| a crowd of people stood and stared
    #
    # A gap here, from 20:30 to 21:00
    #
    11/26/2013 9:00 PM to 11/26/2013 10:30 PM| they'd seen his face before
    11/26/2013 10:00 PM to 11/26/2013 11:00 PM| nobody was really sure ...
    """
    day_in_life = Agenda.from_file(io.StringIO(day_in_life_agtxt))
    day_in_life.normalize()

    # How are we going to test this?  I want to ignore the text descriptions.
    # Defined __eq__ method in Agenda just for this
    should_be_txt = """
    11/26/2013 9:00 AM to 11/26/2013 3:30 PM| I read the news today oh, boy
    11/26/2013 5:00 PM to 11/26/2013 8:30 PM| about a lucky man who made the grade
    11/26/2013 9:00 PM to 11/26/2013 11:00 PM| and though the news was rather sad
    """
    should_be_ag = Agenda.from_file(io.StringIO(should_be_txt))
    assert day_in_life == should_be_ag

    # Start with the simplest cases of "complement"
    simple_agtxt = """12/01/2013 12:00 PM to 12/01/2013 2:00 PM| long lunch"""
    simple_ag = Agenda.from_file(io.StringIO(simple_agtxt))

    # Different day - should have no effect
    tomorrow = Appt.from_string("12/02/2013 11:00 AM to 12/02/2013 3:00 PM| tomorrow")
    simple_ag = simple_ag.complement(tomorrow)
    assert str(simple_ag[0]) ==  "12/02/2013 11:00 AM to 12/02/2013 3:00 PM| tomorrow"

    # And the freeblock should not be altered
    assert str(tomorrow) ==  "12/02/2013 11:00 AM to 12/02/2013 3:00 PM| tomorrow"

    # Freeblock completely covered
    simple_agtxt = """12/01/2013 12:00 PM to 12/01/2013 2:00 PM| long lunch"""
    simple_ag = Agenda.from_file(io.StringIO(simple_agtxt))
    lunch = Appt.from_string("12/01/2013 12:30 PM to 12/01/2013 2:30 PM| lunch")
    simple_ag = simple_ag.complement(lunch)
    assert str(simple_ag) == ""
    # And the freeblock should not be altered
    assert str(lunch) == "12/01/2013 12:30 PM to 12/01/2013 2:30 PM| lunch"
