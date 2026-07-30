import markdown
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from apps.courses.models import Category, Course, Lesson, LessonCompletion, LessonFeedback, LessonBookmark
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

    # Tugatilgan darslar ID larini olish
    completed_lesson_ids = set()
    if request.user.is_authenticated:
        completed_lesson_ids = set(
            LessonCompletion.objects.filter(
                user=request.user,
                lesson__course=course
            ).values_list('lesson_id', flat=True)
        )

    context = {
        'course': course,
        'lessons': lessons,
        'completed_lesson_ids': completed_lesson_ids,
    }
    return render(request, 'courses/course_detail.html', context)

def learning_guide(request):
    courses = Course.objects.all()
    categories = Category.objects.all()
    
    # Map courses by slug for quick lookup in template
    courses_by_slug = {c.slug: c for c in courses}

    context = {
        'courses': courses,
        'categories': categories,
        'courses_by_slug': courses_by_slug,
    }
    return render(request, 'courses/learning_guide.html', context)

def lesson_detail(request, course_slug, lesson_order):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, order=lesson_order)
    next_lesson = Lesson.objects.filter(course=course, order=lesson_order + 1).first()
    prev_lesson = Lesson.objects.filter(course=course, order=lesson_order - 1).first()

    lesson.content = markdown.markdown(
        lesson.content,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite', 
            'markdown.extensions.toc',
            'mdx_math',
        ]
    )

    # Tugatilgan darslar ID larini olish va fikrni yuklash
    completed_lesson_ids = set()
    is_current_completed = False
    user_feedback = None
    is_bookmarked = False
    if request.user.is_authenticated:
        completed_lesson_ids = set(
            LessonCompletion.objects.filter(
                user=request.user,
                lesson__course=course
            ).values_list('lesson_id', flat=True)
        )
        is_current_completed = lesson.id in completed_lesson_ids
        
        feedback_obj = LessonFeedback.objects.filter(user=request.user, lesson=lesson).first()
        if feedback_obj:
            user_feedback = 'like' if feedback_obj.is_helpful else 'dislike'
            
        is_bookmarked = LessonBookmark.objects.filter(user=request.user, lesson=lesson).exists()

    context = {
        'course': course,
        'lesson': lesson,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson,
        'completed_lesson_ids': completed_lesson_ids,
        'is_current_completed': is_current_completed,
        'user_feedback': user_feedback,
        'is_bookmarked': is_bookmarked,
    }
    return render(request, 'courses/lesson_detail.html', context)


@login_required
@require_POST
def toggle_lesson_complete(request, course_slug, lesson_order):
    """Darsni tugatilgan/tugatilmagan deb belgilash."""
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, order=lesson_order)

    completion, created = LessonCompletion.objects.get_or_create(
        user=request.user,
        lesson=lesson,
    )

    if not created:
        # Agar avval tugatilgan bo'lsa — bekor qilish
        completion.delete()

    # Foydalanuvchini qaytarish
    redirect_to = request.POST.get('redirect_to', '')
    if redirect_to:
        return redirect(redirect_to)
    return redirect('lesson_detail', course_slug=course.slug, lesson_order=lesson.order)

@login_required
@require_POST
def toggle_lesson_feedback(request, course_slug, lesson_order):
    """API for toggling lesson feedback (like/dislike)"""
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, order=lesson_order)
    
    try:
        data = json.loads(request.body)
        feedback_type = data.get('type') # 'like' or 'dislike'
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    
    if feedback_type not in ['like', 'dislike']:
        return JsonResponse({'status': 'error', 'message': 'Invalid type'}, status=400)
        
    is_helpful = True if feedback_type == 'like' else False
    
    feedback, created = LessonFeedback.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'is_helpful': is_helpful}
    )
    
    if not created:
        if feedback.is_helpful == is_helpful:
            # User clicked the same button again, remove feedback
            feedback.delete()
            return JsonResponse({'status': 'success', 'action': 'removed'})
        else:
            # User changed their mind
            feedback.is_helpful = is_helpful
            feedback.save()
            return JsonResponse({'status': 'success', 'action': 'updated', 'type': feedback_type})
            
    return JsonResponse({'status': 'success', 'action': 'added', 'type': feedback_type})

@login_required
@require_POST
def toggle_lesson_bookmark(request, course_slug, lesson_order):
    """API for toggling lesson bookmark"""
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, order=lesson_order)
    
    bookmark, created = LessonBookmark.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )
    
    if not created:
        bookmark.delete()
        return JsonResponse({'status': 'success', 'action': 'removed'})
        
    return JsonResponse({'status': 'success', 'action': 'added'})