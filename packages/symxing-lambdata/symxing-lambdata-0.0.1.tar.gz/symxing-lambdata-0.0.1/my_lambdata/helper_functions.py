class Nulls():
    def __init__(self, df):
        self.df = df

    def null_count(self):
        '''
        Sum together all NaNs in a Data Frame
        '''
        print("Here is the sum of the Nulls")

if __name__ == "__main__":
    num_of_nulls = Nulls(df = "url")
    print("At least the code works")

def train_test_split(df, frac):
    
    '''
    IDK what I'm doing?
    '''