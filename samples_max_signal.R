args <- commandArgs(trailingOnly = TRUE)

if (length(args) != 2)
{
	stop("usage: Rscript samples_max_signal.R cluster_profile.txt output_dir")
}

profile_file <- args[1]

if (!file.exists(profile_file))
{
	stop(paste(profile_file, "does not exist."))
}

output_dir <- args[2]

if (!file.exists(output_dir))
{
	stop(paste(output_dir, "does not exist."))
}


cluster_name <- gsub("_profile.txt", "", basename(profile_file))
output_file <- paste(output_dir, paste(cluster_name, 'max_signal_samples.txt', sep='.'), sep="/")

profile <- read.table(profile_file, header=F, row.names=1)

sink(output_file)
samples_max_signal <- table(c(apply(X=profile, MARGIN=1, FUN=which.max)))
samples_max_signal[order(samples_max_signal, decreasing=T)]



#order(c(3,1,2), decreasing=T)
