# R Cheatsheet
## Lab-related
### Import BCA assay reads from Tecan SpectraFluor Excel output
Load required lirbaries:
```R
install.packages("ggplot2", repos="https://cran.r-project.org")
install.packages("RColorBrewer", repos="https://cran.r-project.org")
install.packages("xlsx", repos="https://cran.r-project.org")
install.packages("reshape", repos="https://cran.r-project.org")
library(ggplot2)
library(RColorBrewer)
library(xlsx)
library(reshape)
```

Set working directory and read the Tecan file:

_Note: This assumes that the read for well A1 from the 96-well plate is found in spreadsheet cell B12. Adjust rowIndex and colIndex as appropriate._
```R
setwd('J:/Project/Subfolder/')
bca_date <- read.xlsx('Expt_Folder/BCA_Assay_Spreadsheet.xlsx',
                      sheetIndex = 1,
                      rowIndex = c(12:19),
                      colIndex = c(2:13),
                      header = FALSE)
```

Assuming the assay was done in triplicate with replicates laid out horizontally, identify the standard curve and caluclate the best fit line:
```R
# BCA standard curve manufacturer's recommended protocol:
bca.standards.ng.ul <- data.frame('std.conc'=c(2000,
                         1500,
                         1000,
                         750,
                         500,
                         250,
                         125,
                         25,
                         0))

# Re-name the columns to match so they can be bound together
names(bca_date) <- rep('abs', 12)

# Nine-point standard curve, eight rows in first three columns, plus one row in columns 4-6
bca_date.std.abs <- rbind(bca_date[1:8, 1:3],
                          bca_date[1, 4:6])

# Re-name these again
names(bca_date.std.abs) <- rep('abs', 3)

# Match absorbance reads to corresponding standard value
bca_date.std <- cbind(bca.standards.ng.ul,
                      bca_date.std.abs)

# Re-shape the data frame so that each row is a one standard value-absorbance pair instead of one standard value and three absorbance reads
bca_date.standards <- melt(bca_date.std, id='std.conc')

# Re-name the "value" column to "abs"
names(bca_date.standards)[3] <- 'abs'

# Calulate linear fit
# Output: bca_date.lm$coefficients[1] = intercept
# Output: bca_date.lm$coefficients[2] = slope
bca_date.lm <- lm(abs ~ std.conc, bca_date.standards)
```

Grab the reads for the samples:
```R
# This could be tidied up a bit
bca_date.samples <- data.frame(
    'sample' = c(rep('cond1', 3),
                 rep('cond2', 3),
                 rep('cond3', 3),
                 rep('cond4', 3)),
    'abs' = c(bca_date[2,4],
              bca_date[2,5],
              bca_date[2,6],
              bca_date[3,4],
              bca_date[3,5],
              bca_date[3,6],
              bca_date[4,4],
              bca_date[4,5],
              bca_date[4,6],
              bca_date[5,4],
              bca_date[5,5],
              bca_date[6,6])
)
```

Caluclate the actual protein concentration:
```R
dilution.factor <- 10
bca_date.samples$prot_conc <- dilution.factor * ((bca_date.samples$abs - bca_date.lm$coefficients[1]) / bca_date.lm$coefficients[2])
```
