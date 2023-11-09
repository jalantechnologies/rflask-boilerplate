#!/bin/bash

kubectl rollout status deploy/"$KUBE_APP"-deployment -n "$KUBE_NS"
