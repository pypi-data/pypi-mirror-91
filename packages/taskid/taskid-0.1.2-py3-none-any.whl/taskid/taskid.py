from .task import Task

class Taskid:
    @staticmethod
    def get_tasks():
        return [{
          "id": cls.__name__,
          "name": cls.name(),
          "description": cls.description()
        } for cls in Task.__subclasses__()]

    def get_task(task_id):
        task = Taskid.__find_task(task_id)

        # Return None if no task found

        return {
          "id": task.__name__,
          "name": task.name(),
          "description": task.description(),
          "inputs": task.inputs()
        }

    def run_task(task_id, inputs):
        task = Taskid.__find_task(task_id)

        return task.run(inputs)

    @staticmethod
    def __find_task(task_id):
        return next((cls for cls in Task.__subclasses__() if cls.__name__ == task_id), None)


