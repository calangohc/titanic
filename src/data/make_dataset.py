# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()


def add_title(df):
    """
    Add Title to DataFrame (Mr., Miss., etc)

    :param df: Input Titanic DataFrame (with Name column)
    :return: df with ['Title'] column
    """

    # Creates 'names' pd.Series
    names = df['Name']

    # Split 'names' by ', ' and get the latter value
    proc_names = names.str.split(', ').str[-1]

    # Sets ['Title'] by splitting 'proc_names' by ' ' and getting first value
    df['Title'] = proc_names.str.split(' ').str[0]

    # Returns df
    return df


def add_infant_status(df):
    """
        Add 'Male Infant' and 'Female Infant' categories

        :param df: Input Titanic DataFrame (with Name column)
        :return: df with [['Male Infant','Female Infant']]
        """
    # Get Maximum age to max out for loop
    max_age = df['Age'].max()

    # Get Survival rates by gender
    male_survival_mean = df[df['Sex'] == 'male']['Survived'].mean()
    female_survival_mean = df[df['Sex'] == 'female']['Survived'].mean()

    # Instantiates variables
    global_mean_male, global_mean_female, optimal_male_age, optimal_female_age = None, None, 0, 0

    # Test all possible age divisions for infants to check out which is the threshold that is better than average
    for age in range(0, int(max_age) + 1):

        # Instantiates 'temp_df'
        temp_df = df[df['Age'] < age]

        # TODO checkout warning issued here
        # Instantiates 'male_df'
        male_df = temp_df[(temp_df['Sex'] == 'male') & (df['Age'] > optimal_male_age)]
        male_count = male_df.count().max()

        # Runs code only if sample is not zero
        if male_count > 0:
            infant_mean_male = male_df['Survived'].mean()

            # If average for this age bracket is better, change optimal age
            if infant_mean_male > male_survival_mean:
                optimal_male_age = age

        # Instantiates 'female_df'
        female_df = temp_df[(temp_df['Sex'] == 'female') & (df['Age'] > optimal_female_age)]
        female_count = female_df.count().max()

        # Runs code only if sample is not zero
        if female_count > 0:
            infant_mean_female = female_df['Survived'].mean()

            # If average for this age bracket is better, change optimal age
            if infant_mean_female > female_survival_mean:
                print(age, infant_mean_female)
                optimal_female_age = age

    # Sets new columns to df
    df['Male Infant'] = df['Age'] < optimal_male_age
    df['Female Infant'] = df['Age'] < optimal_female_age

    # Returns df
    return df
