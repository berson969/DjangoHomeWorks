import pytest

from rest_framework.test import APIClient
from model_bakery import baker
from rest_framework import status

from students.models import Student, Course

URL = '/api/v1/courses/'


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, make_m2m=True, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, make_m2m=True, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_retrieve_course(client, course_factory):
    course = course_factory()
    response = client.get(f'{URL}{course.id}/')
    assert response.status_code == 200
    assert response.data['name'] == course.name


@pytest.mark.django_db
def test_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(URL)
    assert response.status_code == 200
    assert len(response.data) == 10


@pytest.mark.django_db
def test_filter_id_course(client, course_factory):
    courses = course_factory(_quantity=10)
    queryset = Course.objects.filter(id=courses[5].id)
    response = client.get(f"{URL}{queryset[0].id}/")
    assert response.status_code == 200
    assert response.data['name'] == courses[5].name


@pytest.mark.django_db
def test_filter_name_course(client, course_factory):
    courses = course_factory(_quantity=10)
    queryset = Course.objects.filter(name=courses[3].name)
    response = client.get(f"{URL}{queryset[0].id}/")
    assert response.status_code == 200
    assert response.data['name'] == courses[3].name


@pytest.mark.django_db
def test_create_course(client):
    data = {'name': 'Test'}
    response = client.post(URL, data)
    assert response.status_code == 201
    assert response.data['name'] == data['name']


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory()
    data = {'name': 'Test'}
    response = client.patch(f"{URL}{course.id}/", data)
    assert response.status_code == 200
    assert response.data['name'] == data['name']


@pytest.mark.django_db
def test_destroy_course(client, course_factory):
    course = course_factory()
    url = f'{URL}{course.id}/'
    response = client.get(url)
    assert response.data['name'] == course.name
    response = client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
@pytest.mark.parametrize(
    ['number_students', 'expected_status'],
    (
            (5, 201),
            (25, 400)
    )

)
def test_max_num_students(client, student_factory, course_factory, number_students, expected_status):
    students = student_factory(_quantity=number_students)
    course = course_factory()
    data_course = {'name': course.name}
    data_students = {'students': [i.id for i in students]}
    response = client.post(URL, data=data_course | data_students)

    assert response.status_code == expected_status
