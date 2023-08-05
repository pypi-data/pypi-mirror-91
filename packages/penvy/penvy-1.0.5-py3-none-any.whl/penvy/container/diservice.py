def diservice(method):
    def wrapper(*args):
        service_name = method.__name__
        container = args[0]

        if service_name not in container.services:
            # print('creating service ' + service_name)
            container.services[service_name] = method(*args)

        return container.services[service_name]

    return wrapper
