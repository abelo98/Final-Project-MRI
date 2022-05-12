from pipeline import Pipeline

def main():
    pipeline = Pipeline('/media/abelo/TERA/School/5to/SRI/PF SRI/Test Collections/20 Newsgroups/20news-18828')
    pipeline.start()
    pipeline.process_query("volvo car")
    print(pipeline.retrive_docs())

   

if __name__ == '__main__':
    main()

