# Loma Verde Aquatic Center (City of Chula Vista) — unofficial preview

A mock-up of the [City of Chula Vista's Loma Verde Aquatic Center page](https://www.chulavistaca.gov/departments/parks-and-recreation/community-centers/loma-verde-aquatic-center)
(the center, Lap & Open Swim, Swim Lessons, Water Fitness, Rentals) with the competition and recreation pools on one live
[Pool Relay](https://www.poolrelay.com) schedule. Not operated by or affiliated with the City of Chula Vista.

No schedule is typed into the pages. Lap swim, open swim, lessons, fitness classes and closures are filled by `finder.js` from the
live Pool Relay view; `build.py` holds only rates, temperatures, policies, office hours and facts about the water.

- `build.py`: generates the five pages.
- `finder.js`: `#today`, `#week`, and `data-live` elements (`hours`, `when`, `exceptions`, `dates`, `closures`).
- Pool Relay view: `1Ublex83fFwpSt76BzsRaI` (Loma Verde Aquatic Center, lane by lane).
