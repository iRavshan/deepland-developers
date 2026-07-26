from django.shortcuts import render, get_object_or_404
from apps.courses.models import Category, Course, Lesson
from apps.users.models import UserProfile

def home(request):
    featured_courses = Course.objects.filter(is_featured=True)[:6]
    categories = Category.objects.all()
    recent_courses = Course.objects.all().order_by('-created_at')[:4]

    context = {
        'featured_courses': featured_courses,
        'categories': categories,
        'recent_courses': recent_courses,
        'total_courses': Course.objects.count(),
        'total_lessons': Lesson.objects.count(),
    }
    return render(request, 'courses/home.html', context)

def course_list(request):
    category_slug = request.GET.get('category')
    courses = Course.objects.all()
    categories = Category.objects.all()

    if category_slug:
        courses = courses.filter(category__slug=category_slug)

    context = {
        'courses': courses,
        'categories': categories,
        'selected_category': category_slug,
    }
    return render(request, 'courses/course_list.html', context)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    lessons = course.lessons.all()
    context = {
        'course': course,
        'lessons': lessons,
    }
    return render(request, 'courses/course_detail.html', context)

def lesson_detail(request, course_slug, lesson_order):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, order=lesson_order)
    next_lesson = Lesson.objects.filter(course=course, order=lesson_order + 1).first()
    prev_lesson = Lesson.objects.filter(course=course, order=lesson_order - 1).first()

    context = {
        'course': course,
        'lesson': lesson,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson,
    }
    return render(request, 'courses/lesson_detail.html', context)