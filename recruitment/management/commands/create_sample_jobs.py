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
                - Bachelor's degree in Computer Science or related field
                ''',
                'salary_range': '$300 - $400/month'  # Thêm lương
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
                'salary_range': '$250 - $350/month'  # Thêm lương
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
                'salary_range': '$300 - $400/month'  # Thêm lương
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
                'salary_range': '$350 - $450/month'  # Thêm lương
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
                'salary_range': '$250 - $350/month'  # Thêm lương
            }
        ]
        
        # Create positions
        for position_data in positions:
            position, created = Position.objects.get_or_create(
                title=position_data['title'],
                defaults={
                    'description': position_data['description'],
                    'requirements': position_data['requirements'],
                    'salary_range': position_data['salary_range'],  # Thêm lương
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created position: {position.title}'))
            else:
                # Cập nhật thông tin lương cho các vị trí đã tồn tại
                position.salary_range = position_data['salary_range']
                position.save()
                self.stdout.write(self.style.WARNING(f'Updated position: {position.title}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created/updated {len(positions)} sample positions'))