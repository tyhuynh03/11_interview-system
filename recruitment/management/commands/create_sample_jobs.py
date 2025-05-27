from django.core.management.base import BaseCommand
from recruitment.models import Position

class Command(BaseCommand):
    help = 'Creates sample job positions'

    def handle(self, *args, **kwargs):
        # List of sample positions
        positions = [
            {
                'title': 'Senior Python Developer',
                'description': '''
                We are looking for an experienced Python Developer to join our growing team. 
                You will be responsible for developing and maintaining high-quality applications.
                
                Responsibilities:
                - Design, build, and maintain efficient, reusable, and reliable Python code
                - Implement security and data protection measures
                - Integration of user-facing elements with server-side logic
                - Integration of data storage solutions
                ''',
                'requirements': '''
                - 5+ years of experience in Python development
                - Strong knowledge of Python web frameworks (Django, Flask)
                - Understanding of object-relational mapping (ORM)
                - Familiarity with front-end technologies (JavaScript, HTML5, CSS3)
                - Knowledge of user authentication and authorization
                - Understanding of fundamental design principles
                - Proficient understanding of code versioning tools (Git)
                - Bachelor's degree in Computer Science or related field                 ''',
                'salary_range': '$300 - $400/month',
                'employment_type': 'full_time',
                'department': 'Engineering'  # Thêm phòng ban
            },
            {
                'title': 'Frontend Developer (React)',
                'description': '''
                We're seeking a talented Frontend Developer with React experience to create 
                responsive and interactive web applications.
                
                Responsibilities:
                - Develop new user-facing features using React.js
                - Build reusable components and front-end libraries for future use
                - Translate designs and wireframes into high-quality code
                - Optimize components for maximum performance
                ''',
                'requirements': '''
                - 3+ years of experience with React.js
                - Thorough understanding of React.js and its core principles
                - Experience with popular React workflows (Redux, Hooks)
                - Strong proficiency in JavaScript, including DOM manipulation and the JavaScript object model
                - Thorough understanding of responsive design and mobile-first approach
                - Experience with common front-end development tools such as Babel, Webpack, NPM, etc.
                - Familiarity with RESTful APIs and modern authorization mechanisms
                ''',
                'salary_range': '$250 - $350/month',
                'employment_type': 'full_time',
                'department': 'Frontend Development'  # Thêm phòng ban
            },
            {
                'title': 'DevOps Engineer',
                'description': '''
                We are looking for a DevOps Engineer to help us build and maintain our cloud infrastructure 
                and deployment pipelines.
                
                Responsibilities:
                - Implement and manage CI/CD pipelines
                - Manage and improve our cloud infrastructure
                - Automate manual processes
                - Monitor systems and applications
                - Troubleshoot and resolve issues in development, testing, and production environments
                ''',
                'requirements': '''
                - 3+ years of experience in a DevOps role
                - Strong knowledge of cloud services (AWS, Azure, or GCP)
                - Experience with infrastructure as code tools (Terraform, CloudFormation)
                - Experience with containerization technologies (Docker, Kubernetes)
                - Knowledge of CI/CD tools (Jenkins, GitLab CI, GitHub Actions)
                - Scripting skills (Python, Bash)
                - Understanding of networking concepts
                ''',
                'salary_range': '$300 - $400/month',
                'employment_type': 'contract',
                'department': 'DevOps'  # Thêm phòng ban
            },
            {
                'title': 'Data Scientist',
                'description': '''
                We're looking for a Data Scientist to analyze large datasets and build predictive models 
                to help drive business decisions.
                
                Responsibilities:
                - Analyze large amounts of data to discover insights and trends
                - Build and implement machine learning models
                - Work with stakeholders to understand business objectives
                - Present findings to non-technical audiences
                - Develop data-driven solutions to business challenges
                ''',
                'requirements': '''
                - Master's or PhD in Statistics, Mathematics, Computer Science, or related field
                - 3+ years of experience in data science or related field
                - Strong knowledge of statistical analysis and machine learning techniques
                - Proficiency in Python or R and data manipulation libraries
                - Experience with data visualization tools
                - Knowledge of SQL and database systems
                - Strong problem-solving skills and attention to detail
                ''',
                'salary_range': '$350 - $450/month',
                'employment_type': 'full_time',
                'department': 'Data Science'  # Thêm phòng ban
            },
            {
                'title': 'UI/UX Designer',
                'description': '''
                We are seeking a creative UI/UX Designer to create amazing user experiences for our products.
                
                Responsibilities:
                - Create user flows, wireframes, prototypes, and mockups
                - Design UI elements and components
                - Conduct user research and testing
                - Collaborate with product managers and developers
                - Create and maintain design systems
                ''',
                'requirements': '''
                - 3+ years of experience in UI/UX design
                - Strong portfolio demonstrating UI/UX projects
                - Proficiency in design tools (Figma, Sketch, Adobe XD)
                - Understanding of user-centered design principles
                - Knowledge of HTML, CSS, and JavaScript is a plus
                - Excellent communication and collaboration skills
                - Bachelor's degree in Design, HCI, or related field
                ''',
                'salary_range': '$250 - $350/month',
                'employment_type': 'part_time',
                'department': 'Design'  # Thêm phòng ban
            },
            {
                'title': 'Mobile App Developer (Flutter)',
                'description': '''
                We are looking for a Flutter Developer to build cross-platform mobile applications.
                
                Responsibilities:
                - Develop high-quality mobile applications using Flutter
                - Collaborate with the design team to implement UI/UX
                - Write clean, maintainable, and efficient code
                - Implement state management solutions
                - Integrate with REST APIs and third-party services
                - Optimize app performance and user experience
                ''',
                'requirements': '''
                - 2+ years of experience in mobile app development
                - Strong knowledge of Flutter and Dart
                - Experience with state management (Provider, Bloc, GetX)
                - Understanding of mobile app architecture patterns
                - Knowledge of RESTful APIs and JSON
                - Experience with version control systems
                - Published apps on App Store/Play Store is a plus
                ''',
                'salary_range': '$300 - $400/month',
                'employment_type': 'full_time',
                'department': 'Mobile Development'
            },
            {
                'title': 'Backend Developer (Node.js)',
                'description': '''
                We're seeking a Backend Developer to build scalable server-side applications.
                
                Responsibilities:
                - Design and implement RESTful APIs
                - Develop and maintain server-side applications
                - Implement security and data protection
                - Optimize database queries and performance
                - Write unit tests and documentation
                ''',
                'requirements': '''
                - 3+ years of Node.js development experience
                - Strong knowledge of Express.js framework
                - Experience with MongoDB or PostgreSQL
                - Understanding of RESTful API design
                - Knowledge of authentication and authorization
                - Experience with testing frameworks
                - Familiarity with Docker and microservices
                ''',
                'salary_range': '$300 - $400/month',
                'employment_type': 'full_time',
                'department': 'Backend Development'
            },
            {
                'title': 'QA Engineer',
                'description': '''
                We need a QA Engineer to ensure the quality of our software products.
                
                Responsibilities:
                - Develop and execute test plans and test cases
                - Perform manual and automated testing
                - Report and track software defects
                - Collaborate with development team
                - Create and maintain test documentation
                ''',
                'requirements': '''
                - 2+ years of QA experience
                - Knowledge of testing methodologies
                - Experience with test automation tools
                - Understanding of Agile/Scrum processes
                - Strong analytical and problem-solving skills
                - Experience with bug tracking tools
                - Knowledge of SQL and basic programming
                ''',
                'salary_range': '$250 - $350/month',
                'employment_type': 'full_time',
                'department': 'Quality Assurance'
            },
            {
                'title': 'Product Manager',
                'description': '''
                We're looking for a Product Manager to drive product development and strategy.
                
                Responsibilities:
                - Define product vision and strategy
                - Gather and analyze user requirements
                - Create product roadmaps and specifications
                - Work with development team on implementation
                - Monitor product performance and metrics
                ''',
                'requirements': '''
                - 3+ years of product management experience
                - Strong analytical and problem-solving skills
                - Experience with Agile methodologies
                - Excellent communication skills
                - Knowledge of product analytics tools
                - Understanding of software development process
                - Bachelor's degree in related field
                ''',
                'salary_range': '$400 - $500/month',
                'employment_type': 'full_time',
                'department': 'Product Management'
            },
            {
                'title': 'Security Engineer',
                'description': '''
                We need a Security Engineer to protect our systems and data.
                
                Responsibilities:
                - Implement security measures and protocols
                - Conduct security assessments and audits
                - Monitor and respond to security incidents
                - Develop security policies and procedures
                - Perform vulnerability testing
                ''',
                'requirements': '''
                - 3+ years of security engineering experience
                - Knowledge of security protocols and tools
                - Experience with penetration testing
                - Understanding of network security
                - Familiarity with compliance standards
                - Strong problem-solving skills
                - Relevant security certifications
                ''',
                'salary_range': '$350 - $450/month',
                'employment_type': 'full_time',
                'department': 'Security'
            },
            {
                'title': 'Technical Writer',
                'description': '''
                We're seeking a Technical Writer to create clear and concise documentation.
                
                Responsibilities:
                - Create technical documentation and guides
                - Write API documentation
                - Develop user manuals and tutorials
                - Maintain documentation accuracy
                - Collaborate with development team
                ''',
                'requirements': '''
                - 2+ years of technical writing experience
                - Strong writing and editing skills
                - Knowledge of documentation tools
                - Understanding of technical concepts
                - Experience with version control
                - Attention to detail
                - Bachelor's degree in related field
                ''',
                'salary_range': '$200 - $300/month',
                'employment_type': 'part_time',
                'department': 'Documentation'
            },
            {
                'title': 'Cloud Architect',
                'description': '''
                We need a Cloud Architect to design and implement cloud solutions.
                
                Responsibilities:
                - Design cloud infrastructure solutions
                - Implement cloud migration strategies
                - Optimize cloud costs and performance
                - Ensure cloud security and compliance
                - Provide technical leadership
                ''',
                'requirements': '''
                - 5+ years of cloud architecture experience
                - Strong knowledge of AWS/Azure/GCP
                - Experience with cloud migration
                - Understanding of cloud security
                - Knowledge of infrastructure as code
                - Relevant cloud certifications
                - Strong problem-solving skills
                ''',
                'salary_range': '$450 - $550/month',
                'employment_type': 'full_time',
                'department': 'Cloud Engineering'
            },
            {
                'title': 'AI/ML Engineer',
                'description': '''
                We're looking for an AI/ML Engineer to develop intelligent solutions.
                
                Responsibilities:
                - Develop machine learning models
                - Implement AI solutions
                - Process and analyze data
                - Optimize model performance
                - Deploy models to production
                ''',
                'requirements': '''
                - 3+ years of AI/ML experience
                - Strong knowledge of ML frameworks
                - Experience with Python and data science
                - Understanding of deep learning
                - Knowledge of model deployment
                - Master's degree in related field
                - Strong mathematical background
                ''',
                'salary_range': '$400 - $500/month',
                'employment_type': 'full_time',
                'department': 'AI/ML'
            },
            {
                'title': 'Blockchain Developer',
                'description': '''
                We need a Blockchain Developer to build decentralized applications.
                
                Responsibilities:
                - Develop smart contracts
                - Build DApps
                - Implement blockchain solutions
                - Ensure security of blockchain systems
                - Research new blockchain technologies
                ''',
                'requirements': '''
                - 2+ years of blockchain development
                - Experience with Solidity
                - Knowledge of Ethereum/other blockchains
                - Understanding of cryptography
                - Experience with Web3.js
                - Strong problem-solving skills
                - Bachelor's degree in related field
                ''',
                'salary_range': '$400 - $500/month',
                'employment_type': 'full_time',
                'department': 'Blockchain'
            },
            {
                'title': 'Game Developer (Unity)',
                'description': '''
                We're seeking a Unity Game Developer to create engaging games.
                
                Responsibilities:
                - Develop games using Unity
                - Implement game mechanics
                - Create game assets and animations
                - Optimize game performance
                - Debug and fix issues
                ''',
                'requirements': '''
                - 2+ years of Unity development
                - Strong C# programming skills
                - Experience with 3D/2D game development
                - Knowledge of game design principles
                - Understanding of game physics
                - Portfolio of completed games
                - Bachelor's degree in related field
                ''',
                'salary_range': '$300 - $400/month',
                'employment_type': 'full_time',
                'department': 'Game Development'
            }
        ]
        
        # Create positions
        for position_data in positions:
            position, created = Position.objects.get_or_create(
                title=position_data['title'],
                defaults={
                    'description': position_data['description'],
                    'requirements': position_data['requirements'],
                    'salary_range': position_data['salary_range'],
                    'employment_type': position_data['employment_type'],
                    'department': position_data['department'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created position: {position.title}'))
            else:
                position.salary_range = position_data['salary_range']
                position.employment_type = position_data['employment_type']
                position.department = position_data['department']
                position.save()
                self.stdout.write(self.style.WARNING(f'Updated position: {position.title}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created/updated {len(positions)} sample positions'))