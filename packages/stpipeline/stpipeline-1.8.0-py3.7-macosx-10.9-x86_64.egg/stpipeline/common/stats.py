"""
This shared object is used to collect
different statistics and QA parameters for
the pipeline run.
"""
import json

class Stats():
    """
    Stats is meant to be used
    in different part of the ST pipeline
    to collect information and statistics
    """
    def __init__(self):
        self.input_reads_forward = 0
        self.input_reads_reverse = 0
        self.reads_after_trimming_forward = 0
        self.reads_after_trimming_reverse = 0
        self.reads_after_rRNA_trimming = 0
        self.reads_after_mapping = 0
        self.reads_after_annotation = 0
        self.reads_after_demultiplexing = 0
        self.reads_after_duplicates_removal = 0
        self.genes_found = 0
        self.duplicates_found = 0
        self.pipeline_version = "-"
        self.mapper_tool = "-"
        self.annotation_tool = "-"
        self.demultiplex_tool = "-"
        self.input_parameters = []
        self.max_genes_feature = 0
        self.min_genes_feature = 0
        self.max_reads_feature = 0
        self.min_reads_feature = 0
        self.average_gene_feature = 0
        self.average_reads_feature = 0
    
    def __str__(self):
        return "input_reads_forward: " +  str(self.input_reads_forward) + \
        "\ninput_reads_reverse: " + str(self.input_reads_reverse) + \
        "\nreads_after_trimming_forward: " + str(self.reads_after_trimming_forward) + \
        "\nreads_after_trimming_reverse: " + str(self.reads_after_trimming_reverse) + \
        "\nreads_after_rRNA_trimming: " + str(self.reads_after_rRNA_trimming) + \
        "\nreads_after_mapping: " + str(self.reads_after_mapping) + \
        "\nreads_after_annotation: " + str(self.reads_after_annotation) + \
        "\nreads_after_demultiplexing: " + str(self.reads_after_demultiplexing) + \
        "\nreads_after_duplicates_removal: " + str(self.reads_after_duplicates_removal) + \
        "\ngenes_found: " + str(self.genes_found) + \
        "\nduplicates_found: " + str(self.duplicates_found) + \
        "\npipeline_version: " + str(self.pipeline_version) + \
        "\nmapper_tool: " + str(self.mapper_tool) + \
        "\nannotation_tool: " + str(self.annotation_tool) + \
        "\ndemultiplex_tool: " + str(self.demultiplex_tool) + \
        "\ninput_parameters: " + ''.join([str(x) for x in self.input_parameters]) + \
        "\nmax_genes_feature: " + str(self.max_genes_feature) + \
        "\nmin_genes_feature: " + str(self.min_genes_feature) + \
        "\nmax_reads_feature: " + str(self.max_reads_feature) + \
        "\nmin_reads_feature: " + str(self.min_reads_feature) + \
        "\navergage_gene_feature: " + str(self.average_gene_feature) + \
        "\naverage_reads_feature: " + str(self.average_reads_feature)
        
    def writeJSON(self, filename):
        qa_parameters = {"input_reads_forward" : self.input_reads_forward,
                         "input_reads_reverse" : self.input_reads_reverse,
                         "reads_after_trimming_forward" : self.reads_after_trimming_forward,
                         "reads_after_trimming_reverse" : self.reads_after_trimming_reverse,
                         "reads_after_rRNA_trimming" : self.reads_after_rRNA_trimming,
                         "reads_after_mapping" : self.reads_after_mapping,
                         "reads_after_annotation" : self.reads_after_annotation,
                         "reads_after_demultiplexing" : self.reads_after_demultiplexing,
                         "reads_after_duplicates_removal" : self.reads_after_duplicates_removal,
                         "genes_found" : self.genes_found,
                         "duplicates_found" : self.duplicates_found,
                         "pipeline_version" : self.pipeline_version,
                         "mapper_tool" : self.mapper_tool,
                         "annotation_tool" : self.annotation_tool,
                         "demultiplex_tool" : self.demultiplex_tool,
                         "input_parameters" : ''.join([str(x) for x in self.input_parameters]),
                         "max_genes_feature" : self.max_genes_feature,
                         "min_genes_feature" : self.min_genes_feature,
                         "max_reads_feature" : self.max_reads_feature,
                         "min_reads_feature" : self.min_reads_feature,
                         "avergage_gene_feature" : self.average_gene_feature,
                         "average_reads_feature" : self.average_reads_feature}
                         
                         
        with open(filename, "w") as filehandler:
            json.dump(qa_parameters, filehandler, indent=2, separators=(',', ': '))
   
qa_stats = Stats()         