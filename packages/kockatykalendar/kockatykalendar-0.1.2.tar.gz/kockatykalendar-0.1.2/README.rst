KockatýKalendár Python
======================

.. image:: https://img.shields.io/pypi/v/kockatykalendar.svg
    :target: https://pypi.python.org/pypi/kockatykalendar
    :alt: Latest PyPI version

API, nástroje a utiltky pre prácu a integráciu s Kockatým Kalendárom pre Python.

Inštalácia
----------

Základná verzia tejto knižnice sa dá nainštalovať pomocou pip:

.. code-block::

    pip install kockatykalendar

Ak plánujete používať JSON API Kockatého Kalendára, použite:

.. code-block::

    pip install kockatykalendar[api]

Ak plánujete použiť Django integráciu pre Kockatý Kalendár, použite:

.. code-block::

    pip install kockatykalendar[django]

Ak chcete obe veci, nainštalujte si :code:`kockatykalendar[api,django]`.

Udalosti v kalendári
--------------------

`kockatykalendar` poskytuje Python reprezentáciu udalostí z Kockatého Kalendára. Možno ju využiť na prácu s udalosťami
v kalendári ale aj ich tvorbu.

.. code-block:: python

    from datetime import date
    from kockatykalendar.events import Event, EventType, EventScience, EventContestant

    event = Event()
    event._id = "ksp-sus-1"
    event.name = "KSP sústredenie"
    event.type = EventType.SUSTREDENIE
    event.sciences = [EventScience.INF]
    event.date.start = date(2020, 12, 13)
    event.date.end = date(2020, 12, 20)
    event.contestants.min = EventContestant(EventContestant.SchoolType.STREDNA, 1)
    event.contestants.min = EventContestant(EventContestant.SchoolType.STREDNA, 4)
    event.places = ["TBD"]
    event.organizers = ["trojsten"]
    event.link = "https://ksp.sk/akcie/sustredenia/"
    print(event.to_json())

    event = Event.from_json(...)

API
---

Súčasťou `kockatykalendar` je aj prístup do JSON API Kockatého Kalendára.

.. code-block:: python

    from kockatykalendar.api import get_events, get_current_dataset, get_available_datasets

    get_available_datasets()
    # [
    #   Dataset(start_year=2020,
    #           end_year=2021,
    #           school_year="2020/2021",
    #           filename="2020_21.json"),
    #   ...
    # ]

    get_current_dataset()
    # Dataset(start_year=2020,
    #         end_year=2021,
    #         school_year="2020/2021",
    #         filename="2020_21.json")

    get_events(dataset) # Dataset môže byť: Dataset, filename alebo celá URL.
    # [
    #   Event,
    #   ...
    # ]

Django integrácia
-----------------

**Zatiaľ iba draft, ešte pracujeme na všetkých detailoch implementácie.**

Organizátori môžu poskytovať svoje udalosti do Kockatého Kalendára aj prostredníctvom endpointu na ich stránkach.
V prípade Djanga si stačí zadefinovať jeden alebo viac generátorov, ktoré budú tvoriť obsah kalendára:

.. code-block:: python

    from kockatykalendar.generators import CalendarGenerator
    from kockatykalendar.events import Event, EventType, EventScience

    class NaseSeminareGenerator(CalendarGenerator):
        def items(self):
            return Seminar.objects.all()

        def event(self, item):
            return Event(
                _id="seminar-%d" % item.id,
                name=item.name,
                sciences=[EventScience.MAT],
                type=EventType.SEMINAR,
                oragnizers=["trojsten"],
                places=["online"],
                date=Event.Dates(start=item.start, end=item.end)
            )

Generátor nie je závislý na Djangu, možno ho použiť aj s inými frameworkami, pokiaľ sa dodrží formát výstupu.
Následne treba pridať view do URLconf-u:

.. code-block:: python

    from kockatykalendar.django import kockatykalendar_json

    path("kkalendar.json", kockatykalendar_json, {"generators": [NaseSeminareGenerator()]})
