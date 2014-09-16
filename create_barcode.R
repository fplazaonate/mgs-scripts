plotBarcode <- function (data, main = "") {
	cols <- list()
		cols$val <- c(0, 0, 1e-07, 4e-07, 1.6e-06, 6.4e-06, 2.56e-05, 
				0.0001024, 0.0004096, 0.0016384)
		cols$col <- c("white", "skyblue", "deepskyblue3", "green3", 
				"yellow", "orange", "red", "darkred", "black")
		image(t(data[nrow(data):1, ]), breaks = cols$val, col = cols$col, 
				axes = F, main = main)
									  box()
}

args <- commandArgs(trailingOnly = TRUE)

if (length(args) != 2)
{
	stop("usage: Rscript create_barcode.R cluster_profile.txt output_dir/")
}

profile_file <- args[1]

if (!file.exists(profile_file))
{
	stop(paste(profile_file, "does not exist."))
}

if (!grepl("_profile.txt", profile_file))
{
	stop("Cluster profile should be prefixed by \"profile.txt\"")
}

output_dir <- args[2]

if (!file.exists(output_dir))
{
	stop(paste(output_dir, "does not exist."))
}

library(Cairo)

cluster_name <- gsub("_profile.txt", "", basename(profile_file))
output_file <- paste(output_dir, paste(cluster_name, 'png', sep='.'), sep="/")
prof <- read.delim(profile_file)
prof <- prof[order(rowSums(prof)),]
cat(output_file)
CairoPNG(filename=output_file, width=1280,height=1024)
plotBarcode(prof,main=paste(cluster_name, " , ", nrow(prof)," genes",sep=""))
dev.off()

