if [ $# -lt 1 ]; then
    echo "No service specified"
    exit 1
fi

running_pod=$(sudo kubectl get pods -n archivematica | grep $1 | grep "Running" | head -n1 | awk '{print $1}')

if [ -z "$running_pod" ]; then
    echo "No running pods for service '$1'"
    exit 1
fi

shift

sudo kubectl exec $running_pod -n archivematica -- $@