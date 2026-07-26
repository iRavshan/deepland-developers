from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.courses.models import Category, Course, Lesson
from apps.users.models import UserProfile

class Command(BaseCommand):
    help = 'Seeds initial sample data for Deepland Google Developers style platform'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Google Developers style Deepland platform data...')

        # Categories
        cat_ai, _ = Category.objects.get_or_create(
            slug='ai-ml',
            defaults={'name': 'Artificial Intelligence & ML', 'icon': 'cpu', 'description': 'Deep Learning, PyTorch, TensorFlow, LLMs and Neural Networks.'}
        )
        cat_dsa, _ = Category.objects.get_or_create(
            slug='dsa',
            defaults={'name': 'Data Structures & Algorithms', 'icon': 'code-2', 'description': 'Algorithmic efficiency, Big-O analysis, Dynamic Programming, Graph Theory.'}
        )
        cat_python, _ = Category.objects.get_or_create(
            slug='python',
            defaults={'name': 'Python & Data Science', 'icon': 'terminal', 'description': 'Python programming, NumPy, Pandas, Data Visualization & Scikit-Learn.'}
        )
        cat_cv, _ = Category.objects.get_or_create(
            slug='computer-vision',
            defaults={'name': 'Computer Vision & Real-world AI', 'icon': 'camera', 'description': 'Image Processing, Face Recognition, Object Detection with OpenCV & YOLO.'}
        )

        # Courses
        c1, _ = Course.objects.get_or_create(
            slug='deep-learning-fundamentals',
            defaults={
                'title': 'Deep Learning & Neural Networks Fundamentals',
                'category': cat_ai,
                'description': 'Master the principles of Neural Networks, Backpropagation, Gradient Descent, and building deep learning models with PyTorch.',
                'level': 'intermediate',
                'duration': '14 Hours',
                'total_lessons': 6,
                'rating': 4.95,
                'is_featured': True
            }
        )

        c2, _ = Course.objects.get_or_create(
            slug='dsa-masterclass',
            defaults={
                'title': 'Data Structures & Algorithms Masterclass',
                'category': cat_dsa,
                'description': 'Comprehensive developer guide to Arrays, Linked Lists, Trees, Graphs, Sorting, and Dynamic Programming in Python.',
                'level': 'beginner',
                'duration': '20 Hours',
                'total_lessons': 8,
                'rating': 4.98,
                'is_featured': True
            }
        )

        c3, _ = Course.objects.get_or_create(
            slug='computer-vision-xface',
            defaults={
                'title': 'Computer Vision & Biometric AI: X-FACE Project',
                'category': cat_cv,
                'description': 'Build an end-to-end facial recognition and computer vision diagnostic system using Convolutional Neural Networks (CNNs).',
                'level': 'advanced',
                'duration': '12 Hours',
                'total_lessons': 5,
                'rating': 4.92,
                'is_featured': True
            }
        )

        c4, _ = Course.objects.get_or_create(
            slug='python-for-data-science',
            defaults={
                'title': 'Python for AI & Data Science Engineering',
                'category': cat_python,
                'description': 'Learn data manipulation, vectorization, matrix algebra, and exploratory data analysis using Python, NumPy & Pandas.',
                'level': 'beginner',
                'duration': '10 Hours',
                'total_lessons': 5,
                'rating': 4.88,
                'is_featured': True
            }
        )

        # Lessons for Course 1
        lessons_c1 = [
            ("1. Introduction to Artificial Neural Networks", "Understand the biological inspiration behind artificial perceptrons, weights, biases, and activation functions.", 1),
            ("2. Activation Functions: ReLU, Sigmoid & Softmax", "Explore non-linear activation functions that enable neural networks to solve complex non-linear problems.", 2),
            ("3. Loss Functions and Optimization Techniques", "Learn how Mean Squared Error and Cross-Entropy loss guide Stochastic Gradient Descent (SGD) and Adam optimizers.", 3),
            ("4. Backpropagation & Automatic Differentiation", "Step-by-step mathematical breakdown of the Chain Rule in computing gradients through deep layers.", 4),
            ("5. Building Your First PyTorch Neural Network", "Practical hands-on guide implementing a Multi-Layer Perceptron (MLP) using torch.nn module in Python.", 5),
            ("6. Preventing Overfitting with Dropout & Regularization", "Apply L2 regularization, Dropout layers, and Early Stopping to improve model generalization on test data.", 6),
        ]
        for title, content, order in lessons_c1:
            Lesson.objects.get_or_create(
                course=c1,
                order=order,
                defaults={'title': title, 'content': content, 'duration': '20 mins', 'xp_points': 60}
            )

        # Lessons for Course 2
        lessons_c2 = [
            ("1. Big-O Complexity & Time-Space Tradeoffs", "Analyze runtime efficiency and memory consumption using Asymptotic Big-O notation.", 1),
            ("2. Array Operations & Two-Pointer Strategy", "Master array manipulation, sliding window technique, and two-pointer algorithms.", 2),
            ("3. Linked Lists, Stacks & Queues", "Construct custom linear data structures from scratch and analyze LIFO vs FIFO execution.", 3),
            ("4. Trees & Binary Search Tree (BST) Traversal", "Implement Depth-First Search (Pre-order, In-order, Post-order) and Breadth-First Search (Level-order).", 4),
            ("5. Graph Algorithms: Dijkstra & A* Search", "Model graph representations with Adjacency Lists and find shortest paths across weighted networks.", 5),
        ]
        for title, content, order in lessons_c2:
            Lesson.objects.get_or_create(
                course=c2,
                order=order,
                defaults={'title': title, 'content': content, 'duration': '25 mins', 'xp_points': 50}
            )

        # Admin / Users
        user, created = User.objects.get_or_create(
            username='ravshan',
            defaults={'first_name': 'Ravshan', 'last_name': 'Sodiqov', 'email': 'ravshan@deepland.uz'}
        )
        if created:
            user.set_password('deepland123!')
            user.save()

        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.rank_title = 'Google Developer Expert'
        profile.avatar_url = 'https://api.dicebear.com/7.x/bottts/svg?seed=Ravshan'
        profile.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded Google Developers style Deepland data!'))
