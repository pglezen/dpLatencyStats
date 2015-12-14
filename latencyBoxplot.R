# Generate DataPower latency boxplots by URI
#

# Read in the CSV data.
df <- read.csv('sample6.csv', stringsAsFactors=F)

# Make a latency column containing the maximum of the
# 16 measurement colummns: X1, X2, ..., X16.
#
latencyColumns <- paste(rep('X',16), 1:16, sep='')
df['Latency']  <- apply(df[,latencyColumns], 1, max)

# Send a boxplot to sample6RPlot.png.
#
png(file='sample6RPlot.png')
boxplot(df$Latency ~ df$uri, col='bisque', border='blue',
        xlab='Request URI', ylab='Response (ms)', main='Latency Summary')
dev.off()
