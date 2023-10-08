all:

test:
	rm -rf out
	mcdp-load-libraries -o out -c "rparmake"