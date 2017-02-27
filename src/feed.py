import feedparser
import entry

class Feed:
    base_url = "http://export.arxiv.org/rss/"

    first_class_feeds = [
            # Physics Related Feeds
            ("Astrophysics", "astro-ph"),
            ("Condensed Matter", "cond-mat"),
            ("General Relativity and Quantum Cosmology", "gr-qc"),
            ("High Energy Physics - Experiment", "hep-ex"),
            ("High Energy Physics - Lattice", "hep-lat"),
            ("High Energy Physics - Phenomenology", "hep-ph"),
            ("High Energy Physics - Theory", "hep-th"),
            ("Mathematical Physics", "math-ph"),
            ("Nonlinear Sciences", "nlin"),
            ("Nuclear Experiment", "nucl-ex"),
            ("Nuclear Theory", "nucl-th"),
            ("Physics", "physics"),
            ("Quantum Physics", "quant-ph"),

            ("Mathematics", "math"),
            ("Computer Science", "cs"),
            ("Quantitative Biology", "q-bio"),
            ("Quantitative Finance", "q-fin"),
            ("Statistics", "stat")
        ]

    astro_sub_feeds = [
            ("Astrophysics of Galaxies",                     "astro-ph.GA"),
            ("Cosmology and Nongalactic Astrophysics",       "astro-ph.CO"),
            ("Earth and Planetary Astrophysics",             "astro-ph.EP"),
            ("High Energy Astrophysical Phenomena",          "astro-ph.HE"),
            ("Instrumentation and Methods for Astrophysics", "astro-ph.IM"),
            ("Solar and Stellar Astrophysics",               "astro-ph.SR")
        ]

    cond_mat_sub_feeds = [
            ("Disordered Systems and Neural Networks", "cond-mat.dis-nn"),
            ("Materials Science",                      "cond-mat.mtrl-sci"),
            ("Mesoscale and Nanoscale Physics",        "cond-mat.mes-hall"),
            ("Other Condensed Matter",                 "cond-mat.other"),
            ("Quantum Gases",                          "cond-mat.quant-gas"),
            ("Soft Condensed Matter",                  "cond-mat.soft"),
            ("Statistical Mechanics",                  "cond-mat.stat-mech"),
            ("Strongly Correlated Electrons",          "cond-mat.str-el"),
            ("Superconductivity",                      "cond-mat.supr-con")
        ]

    non_linear_sub_feeds = [
            ("Adaptation and Self-Organizing Systems",  "nlin.AO"),
            ("Cellular Automata and Lattice Gases",     "nlin.CG"),
            ("Chaotic Dynamics",                        "nlin.CD"),
            ("Exactly Solvable and Integrable Systems", "nlin.SI"),
            ("Pattern Formation and Solitons",          "nlin.PS")
        ]

    # Yes, appart from the first class feeds that are already physics
    # related, there is a whole lot of subfeeds
    physics_sub_feeds = [
            ("Accelerator Physics",                       "physics.acc-ph"),
            ("Atmospheric and Oceanic Physics",           "physics.ao-ph"),
            ("Atomic Physics",                            "physics.atom-ph"),
            ("Atomic and Molecular Clusters",             "physics.atm-clus"),
            ("Biological Physics",                        "physics.bio-ph"),
            ("Chemical Physics",                          "physics.chem-ph"),
            ("Classical Physics",                         "physics.class-ph"),
            ("Computational Physics",                     "physics.comp-ph"),
            ("Data Analysis, Statistics and Probability", "physics.data-an"),
            ("Fluid Dynamics",                            "physics.flu-dyn"),
            ("General Physics",                           "physics.gen-ph"),
            ("Geophysics",                                "physics.geo-ph"),
            ("History and Philosophy of Physics",         "physics.hist-ph"),
            ("Instrumentation and Detectors",             "physics.ins-det"),
            ("Medical Physics",                           "physics.med-ph"),
            ("Optics",                                    "physics.optics"),
            ("Physics Education",                         "physics.ed-ph"),
            ("Physics and Society",                       "physics.soc-ph"),
            ("Plasma Physics",                            "physics.plasm-ph"),
            ("Popular Physics",                           "physics.pop-ph"),
            ("Space Physics",                             "physics.space-ph")
        ]

    math_sub_feeds = [
            ("Algebraic Geometry",          "math.AG"),
            ("Algebraic Topology",          "math.AT"),
            ("Analysis of PDEs",            "math.AP"),
            ("Category Theory",             "math.CT"),
            ("Classical Analysis and ODEs", "math.CA"),
            ("Combinatorics",               "math.CO"),
            ("Commutative Algebra",         "math.AC"),
            ("Complex Variables",           "math.CV"),
            ("Differential Geometry",       "math.DG"),
            ("Dynamical Systems",           "math.DS"),
            ("Functional Analysis",         "math.FA"),
            ("General Mathematics",         "math.GM"),
            ("General Topology",            "math.GN"),
            ("Geometric Topology",          "math.GT"),
            ("Group Theory",                "math.GR"),
            ("History and Overview",        "math.HO"),
            ("Information Theory",          "math.IT"),
            ("K-Theory and Homology",       "math.KT"),
            ("Logic",                       "math.LO"),
            ("Mathematical Physics",        "math.MP"),
            ("Metric Geometry",             "math.MG"),
            ("Number Theory",               "math.NT"),
            ("Numerical Analysis",          "math.NA"),
            ("Operator Algebras",           "math.OA"),
            ("Optimization and Control",    "math.OC"),
            ("Probability",                 "math.PR"),
            ("Quantum Algebra",             "math.QA"),
            ("Representation Theory",       "math.RT"),
            ("Rings and Algebras",          "math.RA"),
            ("Spectral Theory",             "math.SP"),
            ("Statistics Theory",           "math.ST"),
            ("Symplectic Geometry",         "math.SG")
        ]

    computer_science_sub_feeds = [
            ("Artificial Intelligence",                         "cs.AI"),
            ("Computation and Language",                        "cs.CL"),
            ("Computational Complexity",                        "cs.CC"),
            ("Computational Engineering, Finance, and Science", "cs.CE"),
            ("Computational Geometry",                          "cs.CG"),
            ("Computer Science and Game Theory",                "cs.GT"),
            ("Computer Vision and Pattern Recognition",         "cs.CV"),
            ("Computers and Society",                           "cs.CY"),
            ("Cryptography and Security",                       "cs.CR"),
            ("Data Structures and Algorithms",                  "cs.DS"),
            ("Databases",                                       "cs.DB"),
            ("Digital Libraries",                               "cs.DL"),
            ("Discrete Mathematics",                            "cs.DM"),
            ("Distributed, Parallel, and Cluster Computing",    "cs.DC"),
            ("Emerging Technologies",                           "cs.ET"),
            ("Formal Languages and Automata Theory",            "cs.FL"),
            ("General Literature",                              "cs.GL"),
            ("Graphics",                                        "cs.GR"),
            ("Hardware Architecture",                           "cs.AR"),
            ("Human-Computer Interaction",                      "cs.HC"),
            ("Information Retrieval",                           "cs.IR"),
            ("Information Theory",                              "cs.IT"),
            ("Learning",                                        "cs.LG"),
            ("Logic in Computer Science",                       "cs.LO"),
            ("Mathematical Software",                           "cs.MS"),
            ("Multiagent Systems",                              "cs.MA"),
            ("Multimedia",                                      "cs.MM"),
            ("Networking and Internet Architecture",            "cs.NI"),
            ("Neural and Evolutionary Computing",               "cs.NE"),
            ("Numerical Analysis",                              "cs.NA"),
            ("Operating Systems",                               "cs.OS"),
            ("Other Computer Science",                          "cs.OH"),
            ("Performance",                                     "cs.PF"),
            ("Programming Languages",                           "cs.PL"),
            ("Robotics",                                        "cs.RO"),
            ("Social and Information Networks",                 "cs.SI"),
            ("Software Engineering",                            "cs.SE"),
            ("Sound",                                           "cs.SD"),
            ("Symbolic Computation",                            "cs.SC"),
            ("Systems and Control",                             "cs.SY")
        ]

    quantitative_biology_sub_feeds = [
            ("Biomolecules",               "q-bio.BM"),
            ("Cell Behavior",              "q-bio.CB"),
            ("Genomics",                   "q-bio.GN"),
            ("Molecular Networks",         "q-bio.MN"),
            ("Neurons and Cognition",      "q-bio.NC"),
            ("Other Quantitative Biology", "q-bio.OT"),
            ("Populations and Evolution",  "q-bio.PE"),
            ("Quantitative Methods",       "q-bio.QM"),
            ("Subcellular Processes",      "q-bio.SC"),
            ("Tissues and Organs",         "q-bio.TO")
        ]

    quantitative_finance_sub_feeds = [
            ("Computational Finance",             "q-fin.CP"),
            ("Economics",                         "q-fin.EC"),
            ("General Finance",                   "q-fin.GN"),
            ("Mathematical Finance",              "q-fin.MF"),
            ("Portfolio Management",              "q-fin.PM"),
            ("Pricing of Securities",             "q-fin.PR"),
            ("Risk Management",                   "q-fin.RM"),
            ("Statistical Finance",               "q-fin.ST"),
            ("Trading and Market Microstructure", "q-fin.TR")
        ]

    statistics_sub_feeds = [
            ("Applications",      "stat.AP"),
            ("Computation",       "stat.CO"),
            ("Machine Learning",  "stat.ML"),
            ("Methodology",       "stat.ME"),
            ("Other Statistics",  "stat.OT"),
            ("Statistics Theory", "stat.TH")
        ]

    def __init__(self, arg):
        self.url = self.base_url

        self.feed = feedparser.parse(self.url)
        self.etag = self.feed.etag

    def update(self, forced = False):
        if forced:
            self.feed = feedparser.parser(self.url)
        else:
            self.feed = feedparser.parser(self.url, etag=self.etag)

        self.etag = self.feed.etag
