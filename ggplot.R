library(reshape)
library(ggplot2)
library(plyr)

pdf("runtimes.pdf")

# Read values from tab-delimited data file 
x <- read.table("runtimes.dat", header=T, sep="\t")
  
x <-melt(x)

x$query <- factor(x$query, levels=rev(unique(as.character(x$query))))

# x$query <- as.factor(x$query) 
# levels(x$query) <- rev(levels(x$query))
       
ggplot(x,aes(x = query,y=value,fill=variable))+geom_bar(width=0.3, stat="identity",position="dodge") +
  coord_flip() + scale_y_sqrt() + theme_bw()+ylab("runtime in seconds (scale_y_sqrt)")+xlab("query")+scale_fill_brewer(palette="Blues", guide = guide_legend(reverse=TRUE))
