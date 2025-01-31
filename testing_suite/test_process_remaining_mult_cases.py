import pytest
from talon import talon
from .helper_fns import  fetch_correct_ID, get_db_cursor
@pytest.mark.integration

class TestIdentifyRemaining(object):

    def test_intergenic(self):
        """ Example where the transcript is an NIC match to an existing one by
            virtue of a new splice donor.
        """
        conn, cursor = get_db_cursor()
        build = "toy_build"
        edge_dict = talon.make_edge_dict(cursor)
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build)
        transcript_dict = talon.make_transcript_dict(cursor, build)
        vertex_2_gene = talon.make_vertex_2_gene_dict(cursor)
        gene_starts, gene_ends = talon.make_gene_start_and_end_dict(cursor, build)
        correct_gene_ID = run_info.genes + 1

        # Construct temp novel gene db
        talon.make_temp_novel_gene_table(cursor, "toy_build")

        chrom = "chrX"
        positions = [ 1, 100, 900, 1000]
        edge_IDs = [ run_info.edge + 1, run_info.edge + 2 ]
        vertex_IDs = [ run_info.vertex + 1, run_info.vertex + 2 ]
        strand = "+"

        gene_ID, transcript_ID, gene_novelty, transcript_novelty, start_end_info = \
                             talon.process_remaining_mult_cases(chrom, positions, 
                                                                strand, edge_IDs, 
                                                                vertex_IDs, 
                                                                transcript_dict,
                                                                gene_starts, gene_ends, 
                                                                edge_dict, location_dict,
                                                                vertex_2_gene, run_info, 
                                                                cursor)

        assert gene_ID == correct_gene_ID
        assert transcript_dict[frozenset(start_end_info["edge_IDs"])] != None
        assert gene_novelty[0][-2] == "intergenic_novel"
        conn.close()

    def test_antisense(self):
        """ Example where the transcript is antisense but contains no known
            splice vertices
        """
        conn, cursor = get_db_cursor()
        build = "toy_build"
        edge_dict = talon.make_edge_dict(cursor)
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build)
        transcript_dict = talon.make_transcript_dict(cursor, build)
        vertex_2_gene = talon.make_vertex_2_gene_dict(cursor)
        gene_starts, gene_ends = talon.make_gene_start_and_end_dict(cursor, build)
        correct_gene_ID = run_info.genes + 1

        # Construct temp novel gene db
        talon.make_temp_novel_gene_table(cursor, "toy_build")

        chrom = "chr2"
        positions = [ 1000, 950, 700, 600]
        edge_IDs = [ run_info.edge + 1, run_info.edge + 2 ]
        vertex_IDs = [ run_info.vertex + 1, run_info.vertex + 2 ]
        strand = "-"

        gene_ID, transcript_ID, gene_novelty, transcript_novelty, start_end_info = \
                             talon.process_remaining_mult_cases(chrom, positions,
                                                                strand, edge_IDs,
                                                                vertex_IDs,
                                                                transcript_dict,
                                                                gene_starts, gene_ends,
                                                                edge_dict, location_dict,
                                                                vertex_2_gene, run_info,
                                                                cursor)
        assert gene_ID == correct_gene_ID
        assert transcript_dict[frozenset(start_end_info["edge_IDs"])] != None
        assert gene_novelty[0][-2] == "antisense_gene"
        conn.close()

    def test_genomic(self):
        """ Example where the transcript overlaps a gene but contains no known
            splice vertices
        """
        conn, cursor = get_db_cursor()
        build = "toy_build"
        edge_dict = talon.make_edge_dict(cursor)
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build)
        transcript_dict = talon.make_transcript_dict(cursor, build)
        vertex_2_gene = talon.make_vertex_2_gene_dict(cursor)
        gene_starts, gene_ends = talon.make_gene_start_and_end_dict(cursor, build)

        # Construct temp novel gene db
        talon.make_temp_novel_gene_table(cursor, "toy_build")

        chrom = "chr1"
        positions = [ 1000, 950, 700, 600]
        edge_IDs = [ run_info.edge + 1, run_info.edge + 2 ]
        vertex_IDs = [ run_info.vertex + 1, run_info.vertex + 2 ]
        strand = "-"

        gene_ID, transcript_ID, gene_novelty, transcript_novelty, start_end_info = \
                             talon.process_remaining_mult_cases(chrom, positions,
                                                                strand, edge_IDs,
                                                                vertex_IDs,
                                                                transcript_dict,
                                                                gene_starts, gene_ends,
                                                                edge_dict, location_dict,
                                                                vertex_2_gene, run_info,
                                                                cursor)
        correct_gene_ID = fetch_correct_ID("TG3", "gene", cursor)
        assert gene_ID == correct_gene_ID
        assert transcript_dict[frozenset(start_end_info["edge_IDs"])] != None
        assert gene_novelty == []
        assert transcript_novelty[-1][-2] == "genomic_transcript"
        conn.close()
