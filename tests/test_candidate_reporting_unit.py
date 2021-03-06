import tests

class TestCandidateReportingUnit(tests.ElectionResultsTestCase):

    def test_zero_votes(self):
        cru = [c for c in self.candidate_reporting_units if c.reportingunitid == '6020']
        for c in cru:
            self.assertEqual(c.votepct, 0.0)
            self.assertEqual(c.votecount, 0.0)

    def test_number_of_parsed_candidate_reporting_units(self):
        self.assertEqual(len(self.candidate_reporting_units), 505)

    def test_composition_of_candidate_reporting_units_json(self):
        cru_dict = self.raw_races['races'][-1]['reportingUnits'][0]['candidates'][1]
        self.assertEqual(cru_dict['first'], 'Jack')
        self.assertEqual(cru_dict['last'], 'Conway')
        self.assertEqual(cru_dict['party'], 'Dem')
        self.assertEqual(cru_dict['candidateID'], '5266')
        self.assertEqual(cru_dict['polID'], '204')
        self.assertEqual(cru_dict['ballotOrder'], 1)
        self.assertEqual(cru_dict['polNum'], '19601')
        self.assertEqual(cru_dict['voteCount'], 426944)

    def test_candidate_reporting_unit_object_inflation(self):
        cru = self.candidate_reporting_units[0]
        self.assertEqual(type(cru).__name__, 'CandidateReportingUnit')
        self.assertEqual(cru.__module__, 'elex.api.api')

    def test_candidate_reporting_unit_get_units_construction(self):
        cru = self.candidate_reporting_units[0]
        self.assertEqual(cru.raceid, '7582')
        self.assertEqual(cru.last, 'Yes')
        self.assertEqual(cru.candidateid, '12480')
        self.assertEqual(cru.polid, '2')
        self.assertEqual(cru.ballotorder, 1)
        self.assertEqual(cru.polnum, '6212')
        self.assertEqual(cru.votecount, 805617)
        self.assertEqual(cru.winner, True)

    def test_candidate_reporting_unit_sums(self):
        reporting_unit = self.reporting_units[0]

        self.assertEqual(len(self.reporting_units), 192)

        candidate_reporting_units = self.candidate_reporting_units[0:2]
        actual_sums_from_json = 805617 + 354769
        sum_candidate_reporting_units = sum([v.votecount for v in candidate_reporting_units])

        # Make sure we got the right race / reporting unit / candidate reporting units.
        # Thankfully, we denormalized the race fields all the way down!
        for cru in candidate_reporting_units:
            self.assertEqual(cru.raceid, '7582')
            self.assertEqual(cru.level, 'state')

        self.assertEqual(candidate_reporting_units[0].votecount / float(reporting_unit.votecount), 0.694266390666554)

        # The highest-level reporting unit votecount and the sum of votes from the
        # candidate reporting units within that reporting unit should be equal.
        self.assertEqual(reporting_unit.votecount, actual_sums_from_json)
        self.assertEqual(sum_candidate_reporting_units, actual_sums_from_json)
        self.assertEqual(sum_candidate_reporting_units, reporting_unit.votecount)

    def test_candidate_reporting_unit_serialization_keys(self):
        cru = self.candidate_reporting_units[1].serialize()
        self.assertEqual(cru['raceid'], '7582')
        self.assertEqual(cru['last'], 'No')
        self.assertEqual(cru['candidateid'], '12481')
        self.assertEqual(cru['polid'], '3')
        self.assertEqual(cru['ballotorder'], 2)
        self.assertEqual(cru['polnum'], '7922')
        self.assertEqual(cru['votecount'], 354769)
        self.assertEqual(cru['winner'], False)

    def test_candidate_reporting_unit_serialization_order(self):
        cru = list(self.candidate_reporting_units[(4*64)+0].serialize())
        self.assertEqual(cru, ['id','unique_id','raceid','racetype','racetypeid','ballotorder','candidateid','description','fipscode','first','incumbent','initialization_data','is_ballot_measure','last','lastupdated','level','national','officeid','officename','party','polid','polnum','precinctsreporting','precinctsreportingpct','precinctstotal','reportingunitid','reportingunitname','runoff','seatname','seatnum','statename','statepostal','test','uncontested','votecount','votepct','winner'])

    def test_unique_ids(self):
        all_ids = list([b.id for b in self.candidate_reporting_units])
        unique_ids = set(all_ids)
        self.assertEqual(len(all_ids), len(unique_ids))