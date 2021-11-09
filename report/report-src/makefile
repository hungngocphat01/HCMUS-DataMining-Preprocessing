# HUNGNGOCPHAT - 19120615
# Đây là file để convert jupyter notebook sang latex rồi compile ra pdf
# Chỉ hoạt động trên *nix 
# Cần phải có docker và phải docker pull texlive/texlive trứoc

PDF:='BaoCaoLab01'
NOTEBOOKS:= report1 report2

$(PDF): main.tex
	rm -rf build
	docker run -it -v "$(shell pwd)":/work --user "$(shell id -u):$(shell id -g)" -w /work texlive/texlive \
		latexmk -f --shell-escape -interaction=nonstopmode -file-line-error -pdf -outdir=build  $<

	$(eval ORIG_PDF:=$(patsubst %.tex,%.pdf,$<))
	mv build/$(ORIG_PDF) .
	mv $(ORIG_PDF) $@.pdf
	mv $@.pdf ../

main.tex: tmp/main.ipynb 
	jupyter nbconvert --to latex $^ --template-file $(shell pwd)/report_template.tex.j2 
	mv tmp/$@ .
	sed -i '/\\begin{Verbatim/ s/\]/,fontsize=\\footnotesize]/g' $@

tmp/main.ipynb: $(patsubst %,%.ipynb,$(NOTEBOOKS))
	rm -f $@
	mkdir -p tmp
	python3 nbconcat.py $^ > $@

.PHONY: clean 
clean: 
	rm -f *.tex
	rm -rf build 
	rm -rf tmp
