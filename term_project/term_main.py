'''
    @name               main.py
    @brief              task scheduler for term project
    @author             tanner, noah
'''

import cotask
import pyb
import controls_gen
import obj_gen

if __name__ == '__main__':

    # create task objects
    controls_task       = cotask.Task(controls_gen.line_follow_gen, "controls task", priority = 3, period = 10, profile = True, trace=False )
    #distance_task       = cotask.Task()
    obj_task            = cotask.Task(obj_gen.obj_hit_gen, "object task", priority = 2, period = 4, profile = True, trace=False  )


    # add tasks to task list
    cotask.task_list.append(controls_task)
    #cotask.task_list.append(distance_task)
    cotask.task_list.append(obj_task)

    print('program starting...')
    print(cotask.task_list)

    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            print('program exited')
            break

    print('\n' + str (cotask.task_list))
    #print(controls_task.get_trace())
    print(obj_task.get_trace())
    print('')

    print('Program Terminated')