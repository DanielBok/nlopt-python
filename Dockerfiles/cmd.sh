#!/bin/bash

images=(manylinux1 manylinux2010)
user=danielbok

while [[ $# -gt 0 ]]; do
	case $1 in
		build)
			for IMG in ${images[@]}; do
				docker image build -t ${user}/${IMG}:latest -f ${IMG}.Dockerfile .
			done
			docker image prune -f
			;;

		push)
			for IMG in ${images[@]}; do
				docker image push ${user}/${IMG}:latest
			done
			;;

		*)
			echo "Unknown command $1"
	esac
	shift
done

