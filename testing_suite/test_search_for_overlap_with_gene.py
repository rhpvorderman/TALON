import pytest
from talon import talon
from .helper_fns import fetch_correct_ID, get_db_cursor
@pytest.mark.dbunit

class TestSearchForOverlapWithGene(object):

    def test_no_match(self):
        """ Example where the supplied interval should not match anything
        """
        conn, cursor = get_db_cursor()
        build = "toy_build"
        talon.make_temp_novel_gene_table(cursor, "toy_build")
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build)

        chrom = "chr1"
        pos = [3000, 4000]
        strand = "+"
        gene_ID, match_strand = talon.search_for_overlap_with_gene(chrom, pos[0],
                                                                   pos[1],
                                                                   strand, cursor,
                                                                   run_info)
        assert gene_ID == None

        # Should get same results for flipped interval
        gene_ID, match_strand = talon.search_for_overlap_with_gene(chrom, pos[0],
                                                                   pos[1],
                                                                   strand, cursor,
                                                                   run_info)
        assert gene_ID == None
        conn.close()

    def test_single_match(self):
        """ Example where the interval overlaps exactly one gene """
        conn, cursor = get_db_cursor()
        build = "toy_build"
        talon.make_temp_novel_gene_table(cursor, "toy_build")
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build)

        chrom = "chr1"
        pos = [0, 1500]
        strand = "+"

        gene_ID, match_strand = talon.search_for_overlap_with_gene(chrom, pos[0],
                                                                   pos[1],
                                                                   strand, cursor,
                                                                   run_info)


        assert gene_ID == fetch_correct_ID("TG1", "gene", cursor)
        assert match_strand == strand
        conn.close()

    def test_same_strand_match_with_two_genes(self):
        """ Example where interval overlaps two genes, one of which is on the 
            same strand. """
        
        conn, cursor = get_db_cursor()
        build = "toy_build"
        talon.make_temp_novel_gene_table(cursor, "toy_build")
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build)

        chrom = "chr1"
        pos = [1500, 910]
        strand = "-"

        gene_ID, match_strand = talon.search_for_overlap_with_gene(chrom, pos[0], 
                                                                   pos[1],
                                                                   strand, cursor, 
                                                                   run_info)

        assert gene_ID == fetch_correct_ID("TG3", "gene", cursor)
        assert match_strand == strand
        conn.close()

    def test_same_strand_match_left_overlap(self):
        """ Example where the overlap is on the same strand. Query start is to 
            the left of the gene, and query end is before the end of the gene. """

        conn, cursor = get_db_cursor()
        build = "toy_build"
        talon.make_temp_novel_gene_table(cursor, "toy_build")
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build)

        chrom = "chr1"
        pos = [550, 1700]
        strand = "-"

        gene_ID, match_strand = talon.search_for_overlap_with_gene(chrom, pos[0],
                                                                   pos[1],
                                                                   strand, cursor,
                                                                   run_info)

        assert gene_ID == fetch_correct_ID("TG3", "gene", cursor)
        assert match_strand == strand
        conn.close()

    def test_antisense_match(self):
        """ Example where interval overlaps one gene in the antisense direction.
        """

        conn, cursor = get_db_cursor()
        build = "toy_build"
        talon.make_temp_novel_gene_table(cursor, "toy_build")
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build)

        chrom = "chr1"
        pos = [1400, 2100]
        strand = "+"
 
        gene_ID, match_strand = talon.search_for_overlap_with_gene(chrom, pos[0],
                                                                   pos[1],
                                                                   strand, cursor,
                                                                   run_info)

        assert gene_ID == fetch_correct_ID("TG3", "gene", cursor)
        assert match_strand == "-"
        conn.close()

    def test_2_genes_same_strand(self):
        """ Example where query overlaps two genes. Must choose the one with 
            more overlap """
 
        conn, cursor = get_db_cursor()
        build = "toy_build" 
        talon.make_temp_novel_gene_table(cursor, "toy_build")
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build)

        chrom = "chr1"
        pos = [800, 5050]
        strand = "+"

        gene_ID, match_strand = talon.search_for_overlap_with_gene(chrom, pos[0],
                                                                   pos[1],
                                                                   strand, cursor,
                                                                   run_info)

        assert gene_ID == fetch_correct_ID("TG1", "gene", cursor)
        assert match_strand == "+"
        conn.close() 


