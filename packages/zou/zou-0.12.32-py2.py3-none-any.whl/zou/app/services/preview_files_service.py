from zou.app.services import

from zou.app.models import Project, Task
from zou.app.services import files_service
from zou.app.utils import movie_utils

def get_preview_file_dimensions(project):
    """
    Return dimensions set at project level or default dimensions if the
    dimensions are not set.
    """
    resolution = project["resolution"]
    height = 1080
    width = None
    if resolution is not None and bool(re.match(r"\d*x\d*", resolution)):
        [width, height] = resolution.split("x")
        width = int(width)
        height = int(height)
    return (width, height)


def get_preview_file_fps(project):
    """
    Return fps set at project level or default fps if the dimensions are not
    set.
    """
    fps = "24.00"
    if project["fps"] is not None:
        fps = "%.2f" % float(project["fps"].replace(",", "."))
    return fps


def get_project_from_preview_file(preview_file_id):
    """
    Get project dict of related preview file.
    """
    preview_file = files_service.get_preview_file_raw(preview_file_id)
    task = Task.get(preview_file.task_id)
    project = Project.get(task.project_id)
    return project.serialize()


def set_preview_file_status():


def prepare_movie(preview_file_id, uploaded_movie_path):
    project = get_project_from_preview_file(instance_id)
    fps = get_preview_file_fps(project)
    (width, height) = get_preview_file_dimensions(project)
    try:
        normalized_movie_path = movie_utils.normalize_movie(
            uploaded_movie_path, fps=fps, width=width, height=height
        )
        file_store.add_movie(
            "previews",
            preview_file_id,
            normalized_movie_path
        )
    except:
        set_preview_file_status_as_crashed(preview_file_id)
    original_tmp_path = movie_utils.generate_thumbnail(normalized_movie_path)
    set_preview_file_status(PreviewFile.StatusEnum.crashed)
    os.remove(uploaded_movie_path)
    os.remove(normalized_movie_path)
