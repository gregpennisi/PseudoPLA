import matplotlib.pyplot as plt
import random

# Takes two coordinate pairs and returns a list containing their
# [slope, y-intercept]
def get_slope_int(p1, p2) :

	slope = round((p2[1] - p1[1]) / (p2[0] - p1[0]), 5)
	intercept = round((p1[1] - (slope * p1[0])), 5)
	return [slope, intercept]

# Target function: f(x) = -3.4x + 0.14
# f(-1) = 3.4 + 0.14
# f(0) = 0.14
# f(1) = -3.26

plt.figure(1)

plt.plot([-1, 1],[3.54, -3.26])
plt.axis([-1, 1, -1, 1])

# Plot 40 random points, marking positive as green circles and negative as red x's
for i in range(40) :
	x_sign = random.random()
	y_sign = random.random()
	cur_val_x = round(random.random(), 5)
	if x_sign >= 0.5 :
		cur_val_x *= -1
	cur_val_y = round(random.random(), 5)
	if y_sign >= 0.5 :
		cur_val_y *= -1

	# Use target function to determine appropriate label
	target_y = round(((-3.4 * cur_val_x) + 0.14), 5)

	if cur_val_y > target_y :
		plt.plot([cur_val_x], [cur_val_y], 'go')

	else :
		plt.plot([cur_val_x], [cur_val_y], 'rx')

# Generate two random [x,y] pairs with each value ranging between -1 and 1
init_x1 = round(random.random(), 5)
if random.random() >= 0.5 :
	init_x1 += -1

init_y1 = round(random.random(), 5)
if random.random() >= 0.5 :
	init_y1 += -1

init_x2 = round(random.random(), 5)
if random.random() >= 0.5 :
	init_x2 += -1

init_y2 = round(random.random(), 5)
if random.random() >= 0.5 :
	init_y2 += -1

# Calculate the function of the line connecting the two random points from above
# This will be the randomized inital hypothesis
init_slope_and_int = get_slope_int([init_x1, init_y1], [init_x2, init_y2])

# Use calculated function to find appropriate y values for h(-1) and h(1)
lineform_y1 = (-1 * init_slope_and_int[0]) + init_slope_and_int[1]
lineform_y2 = init_slope_and_int[0] + init_slope_and_int[1]

# Plot this inital hypothesis line in yellow
plt.plot([-1, 1], [lineform_y1, lineform_y2], 'y')

# Reset plot to focus on figure 2
plt.figure(2)
plt.axis([-1, 1, -1, 1])
plt.plot([-1, 1], [lineform_y1, lineform_y2], 'y')

# Create list of 20 random points, along with 1 or 0 marker depending on their correct label
# Labeling is calculated using the original target function
gen_set = []

for i in range(20) :

	x_sign = random.random()
	y_sign = random.random()
	cur_val_x = round(random.random(), 5)
	if x_sign >= 0.5 :
		cur_val_x *= -1
	cur_val_y = round(random.random(), 5)
	if y_sign >= 0.5 :
		cur_val_y *= -1

	cur_point = [cur_val_x, cur_val_y]

	target_y = round((-3.4 * cur_val_x) + 0.14, 5)

	if cur_val_y > target_y :
		cur_point.append(1)
		plt.plot([cur_val_x], [cur_val_y], 'go')

	else :
		cur_point.append(0)
		plt.plot([cur_val_x], [cur_val_y], 'rx')

	gen_set.append(cur_point)

finished = False # Becomes true once all 20 points have been confirmed to have correct labels
cur_slope = init_slope_and_int[0]
cur_intercept = init_slope_and_int[1]

# Create a list containing 0, 1, 2... 19
point_chooser = []
for k in range(20) :
	point_chooser.append(k)

# Count the number of hypotheses tested
hypo_count = 0

# PLA begins here
while finished != True : # Only breaks once all 20 points have correct labels

	cur_new_labels = []
	random.shuffle(point_chooser) # Randomize list of numbers 0 - 19 in order to pick random points

	# Label each point in gen_set using equation for current hypothesis
	for point in gen_set :

		cur_target_y = round(((cur_slope * point[0]) + cur_intercept), 5)

		if point[1] > cur_target_y :
			cur_new_labels.append(1)
		else :
			cur_new_labels.append(0)

	i = 0

	# Compare these labels to correct labels in gen_set
	while True :

		j = point_chooser[i] # Picks random point
		cur_hypothesis_intercepts = []

		# Calculates coordinates where current hypothesis line intercepts boundaries of plane
		# bounded between -1 and 1 on both axes
		left = round(((cur_slope * -1) + cur_intercept), 5) #(-1, left)
		right = round(((cur_slope * 1) + cur_intercept), 5) #(1, right)
		bottom = round(((-1 - cur_intercept)/cur_slope), 5) #(bottom, -1)
		top = round(((1 - cur_intercept)/cur_slope), 5)     #(top, 1)

		# Finds two points where hypothesis line intercepts boundaries of plane, and saves
		# their coordinates
		if -1 <= left <= 1 :
			cur_hypothesis_intercepts.append([-1, left])
		if -1 <= right <= 1 :
			cur_hypothesis_intercepts.append([1, right])
		if -1 <= bottom <= 1 :
			cur_hypothesis_intercepts.append([bottom, -1])
		if -1 <= top <= 1 :
			cur_hypothesis_intercepts.append([top, 1])

		# For first incorrect label found, move hypothesis toward misclassified point
		if (gen_set[j][2] != cur_new_labels[j]) :

			# Calculate distances between misclassified point and current hypothesis'
			# intercepts with graph boundaries

			#			 (((       x2       -                x1              ) ^  2) + ((     y2       -               y1               ) ^  2)  ^  (1/2))
			dist_1 = round((((gen_set[j][0] - cur_hypothesis_intercepts[0][0]) ** 2) + ((gen_set[j][1] - cur_hypothesis_intercepts[0][1]) ** 2)) ** (1/2), 5)
			dist_2 = round((((gen_set[j][0] - cur_hypothesis_intercepts[1][0]) ** 2) + ((gen_set[j][1] - cur_hypothesis_intercepts[1][1]) ** 2)) ** (1/2), 5)

			# Calculate two new points which will be used to create new hypothesis function

			# First will be adjusted 2% of the distance between misclassified point and closer intercept
			# Second will be adjusted 0.5% of the distance between misclassified point and further intercept
			if dist_1 >= dist_2 :

				# calculate difference in x and y for further distance
				x_dif_far = gen_set[j][0] - cur_hypothesis_intercepts[0][0]
				y_dif_far = gen_set[j][1] - cur_hypothesis_intercepts[0][1]

				# calculate difference in x and y for closer distance
				x_dif_close = gen_set[j][0] - cur_hypothesis_intercepts[1][0]
				y_dif_close = gen_set[j][1] - cur_hypothesis_intercepts[1][1]

				# Generate new coordinates that connect to create new adjusted hypothesis
				new_x1 = gen_set[j][0] + (0.005 * x_dif_far)
				new_y1 = gen_set[j][1] + (0.005 * y_dif_far)

				new_x2 = gen_set[j][0] + (0.02 * x_dif_close)
				new_y2 = gen_set[j][1] + (0.02 * y_dif_close)

				# calculate new hypothesis function, reset loop
				new_hypo_slope_and_int = get_slope_int([new_x1, new_y1], [new_x2, new_y2])
				cur_slope = new_hypo_slope_and_int[0]
				cur_intercept = new_hypo_slope_and_int[1]
				hypo_count += 1
				break

			else :

				# calculate difference in x and y for closer distance
				x_dif_close = gen_set[j][0] - cur_hypothesis_intercepts[0][0]
				y_dif_close = gen_set[j][1] - cur_hypothesis_intercepts[0][1]

				# calculate difference in x and y for further distance
				x_dif_far = gen_set[j][0] - cur_hypothesis_intercepts[1][0]
				y_dif_far = gen_set[j][1] - cur_hypothesis_intercepts[1][1]

				# Generate new coordinates that connect to create new adjusted hypothesis
				new_x1 = gen_set[j][0] + (0.005 * x_dif_far)
				new_y1 = gen_set[j][1] + (0.005 * y_dif_far)

				new_x2 = gen_set[j][0] + (0.02 * x_dif_close)
				new_y2 = gen_set[j][1] + (0.02 * y_dif_close)

				# calculate new hypothesis function, reset loop
				new_hypo_slope_and_int = get_slope_int([new_x1, new_y1], [new_x2, new_y2])
				cur_slope = new_hypo_slope_and_int[0]
				cur_intercept = new_hypo_slope_and_int[1]
				hypo_count += 1
				break

		i += 1

		if i == 20 : # If all 20 points are correctly classified, break out of all loops
			finished = True
			break

# Add final pieces of data to figure 2, and display both figures
lineform_y1 = (-1 * cur_slope) + cur_intercept
lineform_y2 = cur_slope + cur_intercept

plt.plot([-1, 1], [lineform_y1, lineform_y2], 'r')
plt.plot([-1, 1],[3.54, -3.26])
print(hypo_count)
plt.show()
