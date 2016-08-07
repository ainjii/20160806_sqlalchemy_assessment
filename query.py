"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise directions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()

# -------------------------------------------------------------------
# Part 2: Write queries


# Get the brand with the **id** of 8.
Brand.query.filter_by(id=8).all()

# Get all models with the **name** Corvette and the **brand_name** Chevrolet.
# Of course, you don't need to include the brand name because no other brand
# has a model called Corvette
Model.query.filter_by(name='Corvette').filter_by(brand_name='Chevrolet').all()

# Get all models that are older than 1960.
Model.query.filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with "Cor".
Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
Brand.query.filter(Brand.founded == 1903, Brand.discontinued.is_(None)).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
Brand.query.filter(
    (Brand.founded < 1950) |
    (Brand.discontinued.isnot(None))
).all()

# Get any model whose brand_name is not Chevrolet.
Model.query.filter(Model.brand_name != 'Chevrolet').all()

# Fill in the following functions. (See directions for more info.)


def get_model_info(year):
    '''Takes in a year, and prints out each model, brand_name, and brand
    headquarters for that year using only ONE database query.'''

    models = db.session.query(Model.name,
                              Model.brand_name,
                              Brand.headquarters).filter(Model.year == year).outerjoin(Brand).all()

    for model in models:
        print "Model: %s, Brand: %s, HQ: %s" % (model[0],
                                                model[1],
                                                model[2])


def get_brands_summary():
    '''Prints out each brand name, and each model name for that brand
     using only ONE database query.'''

    brands = Brand.query.options(db.joinedload('models')).all()

    for brand in brands:
        print "%s" % brand.name
        print "--------------"

        for model in brand.models:
            print "\t%s" % model.name

        print '=============='

# -------------------------------------------------------------------
# Part 2.5: Discussion Questions (Include your answers as comments.)

# 1. What is the returned value and datatype of ``Brand.query.filter_by(name='Ford')``?
# This will return a Query object, which will filter by Brand.name = 'Ford'.

# 2. In your own words, what is an association table, and what *type* of relationship
# does an association table manage?
# An association table is a table that connects two tables that have a many-to-many
# relationship. In some cases, this table has a logical place in the schema. For example,
# if a user can comment on many Facebook statuses, and a Facebook status can have
# many user comments, then a logical association table is Comments. In other cases,
# the hybrid is not a solid concept that exists in the world, so we make the
# table name a hybrid, like BookGenre.

# -------------------------------------------------------------------
# Part 3


def search_brands_by_name(mystr):
    like_str = '%%%s%%' % mystr
    brands = Brand.query.filter(Brand.name.like(like_str)).all()

    return brands


def get_models_between(start_year, end_year):
    models = Model.query.filter(Model.year >= start_year,
                                Model.year < end_year).all()

    return models
