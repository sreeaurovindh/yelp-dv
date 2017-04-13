db.foodbusiness.aggregate(

	// Pipeline
	[
		// Stage 1
		{
			$unwind: {
			    path : "$categories"
			}
		},

		// Stage 2
		{
			$group: {
			'_id': {
				'state': '$state',
				'city': '$city',
						    },
				'categories': { '$addToSet': '$categories' } 						
			}
		},

		// Stage 3
		{
			$group: {
				'_id': {
					'state': '$_id.state'
				},
				'cities': { '$addToSet': { 'city': '$_id.city', 'category':'$categories' } }
			}
		},
	]
);
