import feedparser
import entry

class Feed:
    base_url = "http://export.arxiv.org/rss/"

    feeds = {
            ## First Class Feeds
            # Physics Related Feeds
            'astro-ph': "Astrophysics",
            'cond-mat': "Condensed Matter",
            'gr-qc':    "General Relativity and Quantum Cosmology",
            'hep-ex':   "High Energy Physics - Experiment",
            'hep-lat':  "High Energy Physics - Lattice",
            'hep-ph':   "High Energy Physics - Phenomenology",
            'hep-th':   "High Energy Physics - Theory",
            'math-ph':  "Mathematical Physics",
            'nlin':     "Nonlinear Sciences",
            'nucl-ex':  "Nuclear Experiment",
            'nucl-th':  "Nuclear Theory",
            'physics':  "Physics",
            'quant-ph': "Quantum Physics",

            'math':  "Mathematics",
            'cs':    "Computer Science",
            'q-bio': "Quantitative Biology",
            'q-fin': "Quantitative Finance",
            'stat':  "Statistics",

            # Astrophysics Sub Feeds
            'astro-ph.GA': "Astrophysics of Galaxies",
            'astro-ph.CO': "Cosmology and Nongalactic Astrophysics",
            'astro-ph.EP': "Earth and Planetary Astrophysics",
            'astro-ph.HE': "High Energy Astrophysical Phenomena",
            'astro-ph.IM': "Instrumentation and Methods for Astrophysics",
            'astro-ph.SR': "Solar and Stellar Astrophysics",

            # Condensed Matter Sub Feeds
            'cond-mat.dis-nn':    "Disordered Systems and Neural Networks",
            'cond-mat.mtrl-sci':  "Materials Science",
            'cond-mat.mes-hall':  "Mesoscale and Nanoscale Physics",
            'cond-mat.other':     "Other Condensed Matter",
            'cond-mat.quant-gas': "Quantum Gases",
            'cond-mat.soft':      "Soft Condensed Matter",
            'cond-mat.stat-mech': "Statistical Mechanics",
            'cond-mat.str-el':    "Strongly Correlated Electrons",
            'cond-mat.supr-con':  "Superconductivity",

            # Non Linear Sub Feeds
            'nlin.AO': "Adaptation and Self-Organizing Systems",
            'nlin.CG': "Cellular Automata and Lattice Gases",
            'nlin.CD': "Chaotic Dynamics",
            'nlin.SI': "Exactly Solvable and Integrable Systems",
            'nlin.PS': "Pattern Formation and Solitons",

            # Physics Sub Feeds
            # Yes, appart from the first class feeds that are already physics
            # related, there is a whole lot of subfeeds
            'physics.acc-ph':   "Accelerator Physics",
            'physics.ao-ph':    "Atmospheric and Oceanic Physics",
            'physics.atom-ph':  "Atomic Physics",
            'physics.atm-clus': "Atomic and Molecular Clusters",
            'physics.bio-ph':   "Biological Physics",
            'physics.chem-ph':  "Chemical Physics",
            'physics.class-ph': "Classical Physics",
            'physics.comp-ph':  "Computational Physics",
            'physics.data-an':  "Data Analysis, Statistics and Probability",
            'physics.flu-dyn':  "Fluid Dynamics",
            'physics.gen-ph':   "General Physics",
            'physics.geo-ph':   "Geophysics",
            'physics.hist-ph':  "History and Philosophy of Physics",
            'physics.ins-det':  "Instrumentation and Detectors",
            'physics.med-ph':   "Medical Physics",
            'physics.optics':   "Optics",
            'physics.ed-ph':    "Physics Education",
            'physics.soc-ph':   "Physics and Society",
            'physics.plasm-ph': "Plasma Physics",
            'physics.pop-ph':   "Popular Physics",
            'physics.space-ph': "Space Physics",

            # Mathematics Sub Feeds
            'math.AG': "Algebraic Geometry",
            'math.AT': "Algebraic Topology",
            'math.AP': "Analysis of PDEs",
            'math.CT': "Category Theory",
            'math.CA': "Classical Analysis and ODEs",
            'math.CO': "Combinatorics",
            'math.AC': "Commutative Algebra",
            'math.CV': "Complex Variables",
            'math.DG': "Differential Geometry",
            'math.DS': "Dynamical Systems",
            'math.FA': "Functional Analysis",
            'math.GM': "General Mathematics",
            'math.GN': "General Topology",
            'math.GT': "Geometric Topology",
            'math.GR': "Group Theory",
            'math.HO': "History and Overview",
            'math.IT': "Information Theory",
            'math.KT': "K-Theory and Homology",
            'math.LO': "Logic",
            'math.MP': "Mathematical Physics",
            'math.MG': "Metric Geometry",
            'math.NT': "Number Theory",
            'math.NA': "Numerical Analysis",
            'math.OA': "Operator Algebras",
            'math.OC': "Optimization and Control",
            'math.PR': "Probability",
            'math.QA': "Quantum Algebra",
            'math.RT': "Representation Theory",
            'math.RA': "Rings and Algebras",
            'math.SP': "Spectral Theory",
            'math.ST': "Statistics Theory",
            'math.SG': "Symplectic Geometry",

            # Computer Science Sub Feeds
            'cs.AI': "Artificial Intelligence",
            'cs.CL': "Computation and Language",
            'cs.CC': "Computational Complexity",
            'cs.CE': "Computational Engineering, Finance, and Science",
            'cs.CG': "Computational Geometry",
            'cs.GT': "Computer Science and Game Theory",
            'cs.CV': "Computer Vision and Pattern Recognition",
            'cs.CY': "Computers and Society",
            'cs.CR': "Cryptography and Security",
            'cs.DS': "Data Structures and Algorithms",
            'cs.DB': "Databases",
            'cs.DL': "Digital Libraries",
            'cs.DM': "Discrete Mathematics",
            'cs.DC': "Distributed, Parallel, and Cluster Computing",
            'cs.ET': "Emerging Technologies",
            'cs.FL': "Formal Languages and Automata Theory",
            'cs.GL': "General Literature",
            'cs.GR': "Graphics",
            'cs.AR': "Hardware Architecture",
            'cs.HC': "Human-Computer Interaction",
            'cs.IR': "Information Retrieval",
            'cs.IT': "Information Theory",
            'cs.LG': "Learning",
            'cs.LO': "Logic in Computer Science",
            'cs.MS': "Mathematical Software",
            'cs.MA': "Multiagent Systems",
            'cs.MM': "Multimedia",
            'cs.NI': "Networking and Internet Architecture",
            'cs.NE': "Neural and Evolutionary Computing",
            'cs.NA': "Numerical Analysis",
            'cs.OS': "Operating Systems",
            'cs.OH': "Other Computer Science",
            'cs.PF': "Performance",
            'cs.PL': "Programming Languages",
            'cs.RO': "Robotics",
            'cs.SI': "Social and Information Networks",
            'cs.SE': "Software Engineering",
            'cs.SD': "Sound",
            'cs.SC': "Symbolic Computation",
            'cs.SY': "Systems and Control",

            # Quantitative Biology Sub Feeds
            'q-bio.BM': "Biomolecules",
            'q-bio.CB': "Cell Behavior",
            'q-bio.GN': "Genomics",
            'q-bio.MN': "Molecular Networks",
            'q-bio.NC': "Neurons and Cognition",
            'q-bio.OT': "Other Quantitative Biology",
            'q-bio.PE': "Populations and Evolution",
            'q-bio.QM': "Quantitative Methods",
            'q-bio.SC': "Subcellular Processes",
            'q-bio.TO': "Tissues and Organs",

            # Quantitative Finance Sub Feeds
            'q-fin.CP': "Computational Finance",
            'q-fin.EC': "Economics",
            'q-fin.GN': "General Finance",
            'q-fin.MF': "Mathematical Finance",
            'q-fin.PM': "Portfolio Management",
            'q-fin.PR': "Pricing of Securities",
            'q-fin.RM': "Risk Management",
            'q-fin.ST': "Statistical Finance",
            'q-fin.TR': "Trading and Market Microstructure",

            # Statistics Sub Feeds
            'stat.AP': "Applications",
            'stat.CO': "Computation",
            'stat.ML': "Machine Learning",
            'stat.ME': "Methodology",
            'stat.OT': "Other Statistics",
            'stat.TH': "Statistics Theory"
            }

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

    def is_valid(feed_name):
        return feed_name in Feed.feeds.keys()
