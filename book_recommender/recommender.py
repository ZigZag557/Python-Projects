


from enum import Enum
import os

AllBooks = []
AllUsers = []



def StartProgram():
	ReadUsers()
	ReadBooks()
	MainMenu()
	

def ReadBooks():
	""" Reads books from books.txt and fills up 'AllBooks' list. """
	booksFile = open("books.txt", "r")
	booksFileData = booksFile.read().split("\n")

	for x in range(len(booksFileData)):
		avg = GetAvgScoreOfBook(x)
		book = Book(booksFileData[x], avg)
		AllBooks.append(book)

	booksFile.close()

def ReadUsers():
	""" Reads users from ratings.txt and fills up AllUsers list. """
	userFile = open("ratings.txt", "r")
	userFileData = userFile.read().split("\n")

	i = 0
	while i < len(userFileData)-1:
		bookRatingsStr = userFileData[i+1].strip()
		userData = User(userFileData[i], bookRatingsStr)
		AllUsers.append(userData)
		i+= 2

	userFile.close()


def doesUserExist(userName):
	""" Checks if the user exists in AllUsers list.
	:param userName: User's name.
	:type userName: string

	:return: Returns true or false if user exists and the user's index in AllUsers list. (-1 if user doesn't exist)
	:rtype: bool|int
	"""

	for x in range(len(AllUsers)):
		if userName == AllUsers[x].GetUserName():
			return True, x
	return False, -1


def GetLikenessPercentage(user1Books, user2Index):

	""" Gets likeness percentage by substracting 10 from the score difference between
	all books and taking average and than turning this average to percentage. 
	(10 being the maximum score difference considering maximum and minimum points
	the user can make are 5 and -5 respectively)

	:param user1Books: First user's book list in AllUsers.
	:type user1Books: int[]

	:param user2Index: Second user's index in AllUsers.
	:type user2Index: int

	:return: Likeness percentage between 0 and 100.
	:rtype: int
	"""
	likenessScore = 0
	likenessScorers = 0
	user2Books = AllUsers[user2Index].GetReadBooks()

	for y in range(len(user1Books)):

		# If one of the users haven't read the book, ignore that user.
		if int(user1Books[y]) == BookStatus.BOOK_NOT_READ.value or int(user2Books[y]) == BookStatus.BOOK_NOT_READ.value:
			continue

		likenessScore += 10 - abs(int(user1Books[y]) - int(user2Books[y]))
		likenessScorers += 1

	# It is possible that the users haven't read any common books, in that case return 0.
	if likenessScorers == 0:
		return 0

	# Percentage calculation:
	return int((likenessScore/likenessScorers) * 10)




def GetAvgScoreOfBook(BookIndex):

	"""Looping through every user's read books in AllUsers list and averaging their score on 
	:param BookIndex: Index of the book in the AllBooks list that it's score going to be averaged.
	:type BookIndex: int

	:return: Average score the user's gave to that book in X.XX format.
	:rtype: float
	"""
	totalScore = 0
	totalScorers = 0
	for y in range(len(AllUsers)):
		usrScore = AllUsers[y].GetReadBooks()[BookIndex]
		if(int(usrScore) != BookStatus.BOOK_NOT_READ.value):
			totalScore += float(AllUsers[y].GetReadBooks()[BookIndex])
			totalScorers += 1.0

	if totalScorers == 0:
		return 0

	# Formatting to show only 2 deciminals.
	return "{:.2f}".format(totalScore / totalScorers)


def MainMenu():

	""" The menu where the user will log in. """
	print("Welcome to the book wizard, please enter your name:")
	while(True):
		answer = input()

		if len(answer) < 3:
			print("Your user name is too short!")
			continue
		elif "\\" in answer:
			print("Please do not use any backslashes.")
			continue 
		break

	userName = answer.strip()
	doesExist, userIndex = doesUserExist(userName)
	
	if doesExist:
		ShowExistingUserMenu(userIndex)
	else:
		RunConsoleNewUser(userName)


def ShowExistingUserMenu(userIndex):

	""" After logging in, if the user already exists in the database, this function will be called. 
		This function will also be called if a new user registers and edit's his/her read books.

	:param userIndex: The user's index in AllUsers that this menu will be for.
	:type userIndex: int
	"""

	userName = AllUsers[userIndex].GetUserName()
	print("-------------------------------------------")
	print("Welcome " + userName + ", if you would like to edit the books you have read, write 'edit'." )
	print("If you would like to log out, write 'out'.")

	# Loop until the user writes a valid command.
	while(True):
		answer = input()
		if(answer == "out"):
			MainMenu()
			break
		elif(answer == "edit"):
			EditReadBooks(userIndex)
			break
		else:
			print("Invalid command.")


def RunConsoleNewUser(userName):

	"""Add user to the list and then go to book editing section.

	:param userName: User's name who is registering.
	:type userName: string
	"""
	print("-------------------------------------------")
	print("Welcome to the book wizard " + userName + "!")
	newUser = User(userName)
	newUser.SetReadNoBooks(len(AllBooks))
	AllUsers.append(newUser)
	EditReadBooks(len(AllUsers) - 1)


def EditReadBooks(userIndex):

	""" Book editing menu in which the user can add or remove books from his/her list. 

	:param userIndex: Index of the user in AllUsers whom book list will be edited.
	:type userIndex: int
	"""

	userBooks = AllUsers[userIndex].GetReadBooks()

	# Loop until the user writes "ok".
	while(True):
		print("-------------------------------------------")
		print("To add a new book, write the index on that book to the console.")
		print("If you would like to remove a book you have read, write 'del X' where X is the index of that book.")
		print("Write 'ok' when you are finished.", end="\n\n")

		PrintReadAndUnreadBooks(userBooks)
		answer = input()

		if(answer == "ok"):
			# Saving the user data.
			AllUsers[userIndex].SetReadBooks(userBooks)
			SaveUserData()
			break

		if(answer[0:3] == "del"):
			indexToRemove = answer.split(" ")[1]
			if(isValidInt(indexToRemove) and userBooks[int(indexToRemove)-1] != BookStatus.BOOK_NOT_READ.value ):
				userBooks[int(indexToRemove)-1] = BookStatus.BOOK_NOT_READ.value

		if(isValidInt(answer) and int(answer) > 0 and int(answer) <= len(AllBooks) and int(userBooks[int(answer) - 1]) == BookStatus.BOOK_NOT_READ.value):
		# Because all books list indices start from 1 instead of 0 for the user to not get confused..
		# ..real book index will be 1 less the selected index.
			selectedIndex = int(answer) - 1

			# Keep repeating until the user has given an available score to the book or aborted.
			while(True):
				print("---------------------------------------")
				print("Book: " + AllBooks[selectedIndex].GetName())
				print("Please write your score from -5 to 5. (0 is not allowed.)")
				print("To abort, write 'abort'.")

				answer = input()


				if answer == "abort":
					break

				# Checking if the score is an expected number.
				if (isValidInt(answer) and int(answer) <= 5 and int(answer) >= -5 and int(answer) != 0):
					selectedScore = int(answer)
					userBooks[selectedIndex] = selectedScore
					print("Added the book to the list.", end="\n---------------------\n")
					break


	# Checking if the user has any books in his/her list.
	if(GetReadBookAmount(userBooks) != 0):
		requestedApproach = GetRequestedApproachType()
		PrintRecommendedBooks(userBooks, requestedApproach)
	else:
		print("Because you don't have any books in your list, we can not recommend you new books.")

	print("\nYour book list has been saved to the database.\n")

	# Go back to the user menu.
	ShowExistingUserMenu(userIndex)


def GetReadBookAmount(userBooks):
	""" Return how many books the user has read.

	:param userBooks: User's book list.
	:type userBooks: int[]

	:return: User's read book amount.
	:rtype: int
	"""
	totalRead = 0
	for x in userBooks:
		if int(x) != BookStatus.BOOK_NOT_READ.value:
			totalRead += 1
	return totalRead


def isValidInt(strValue):
	""" Returns true if the input is an integer.
		This function is used instead of isnumeric() because that function doesn't work with negative numbers.

	:param strValue: String to be checked if is a number.
	:type strValue: string

	:return: True or false, if the string is a number or not.
	:rtype: bool
	"""

	try:
		int(strValue)
		return True
	except ValueError:
		return False


def GetRequestedApproachType():
	""" Gets the requested approach type.

	:return: Choosen approach type. "a", "b" or "c". 
	:rtype: string
	"""
	selectedAlgorithm = ""

	while(True):
		print("Which approach would you like to be used for recommendations? 'A', 'B', 'C'?")
		answerArray = ["a", "b", "c"]
		answer = input().lower()
		if(answer in answerArray):
			selectedAlgorithm = answer.lower()
			break
			
	return answer.lower()


def SaveUserData():

	""" Saves the AllRatings list into ratings.txt.
		Saves the list into ratings_tmp.txt first to avoid file corruption while writing data just in case.
	"""

	tmpFile = open("ratings_tmp.txt", "a+")
	for x in range(len(AllUsers)):
		tmpFile.write(AllUsers[x].GetUserName() + "\n")

		usrReadBooks = AllUsers[x].GetReadBooks()
		# scoresstr will be the str version of the read books array that's going to be written into the file.
		scoresStr = ""
		for y in range(len(usrReadBooks)):
			scoresStr += " " + str(AllUsers[x].GetReadBooks()[y])

		# [1:0] to remove the extra white space on left side of the string.
		tmpFile.write(scoresStr[1:] + "\n")

	tmpFile.close()
	os.remove("ratings.txt")
	os.rename("ratings_tmp.txt", "ratings.txt")


def PrintRecommendedBooks(userBooks, approachStr):

	""" Prints recommended books in selected approach.
		
	:param userBooks: The main user's book list that will get recommendations.
	:type userBooks: int[]

	:param approachStr: Approach type that's going to be used.
	:type approachStr: string
	"""

	recommendedBooksList = []
	print("-----------------------------------")
	print("Recommended books:")

	# recommendedBooksList will be made of Book objects.
	# Higher the average score, the upper in the recommendation list the book will be.

	if(approachStr == "a"):
		recommendedBooksList = GetRecommendedBooksA()
	elif(approachStr == "b"):
		recommendedBooksList = GetRecommendedBooksB(userBooks)
	elif(approachStr == "c"):
		recommendedBooksList = GetRecommendedBooksC(userBooks)


	recommendedBooksList = sorted(recommendedBooksList, key=lambda obj: obj.GetAvgScore(), reverse = True)

	# Show top 10 recommendations.
	# If there are less than 10 recommendations, show all.
	booksLen = len(recommendedBooksList)
	if booksLen > 10:
		booksLen = 10

	for x in range(booksLen):
		print(recommendedBooksList[x].GetName())



def GetRecommendedBooksA():
	""" Approach A: Returns AllBooks list. 
		Books in AllBooks list already have their average score's set by
		ReadBooks function. No further operation needed.

	:return: AllBooks list.
	:rtype: Book[]
	"""
	return AllBooks

def GetRecommendedBooksB(userBooks):

	""" Approach B: Find the person with highest likeness percentage and return that user's read books.
	
	:param userBooks: The user's book list whom will get recommended books.
	:type userBooks: int[]

	:return: Book list of the most similiar user.
	:rtype: Book[]
	"""

	highestLikenessPercentage = 0
	mostSimiliarScoreList = None

	for x in range(len(AllUsers)):
		likeness = GetLikenessPercentage(userBooks, x)
		if likeness > highestLikenessPercentage:
			mostSimiliarScoreList = AllUsers[x].GetReadBooks()
			highestLikenessPercentage = likeness

	bookList = []
	for x in range(len(mostSimiliarScoreList)):
		book = Book(AllBooks[x].GetName(), mostSimiliarScoreList[x])
		bookList.append(book)
	return bookList

def GetRecommendedBooksC(userBooks):

	""" Approach C: Get recommendations with the consideration of all user's likeness to the user and their scores.
		For each book, get's weighted average of scores all users gave, weight being their likeness percentage.

	:param userBooks: The user's book list whom will get recommended books.
	:type userBooks: int[]

	:return: Book list with average score being weighted average of the user's ratings. If the user has no books in his/her list, return empty list.
	:rtype: Book[]
	"""
	recommendedBooks = []

	for y in range(len(AllBooks)):
		totalScore = 0
		totalPercentage = 0

		for x in range(len(AllUsers)):

			# If the user haven't read the book, skip the user.
			if int(AllUsers[x].GetReadBooks()[y]) == BookStatus.BOOK_NOT_READ.value:
				continue
			
			likeness = GetLikenessPercentage(userBooks, x)

			# If the likeness percentage lower that 40, ignore that user's score.
			if(likeness < 40):
				continue

			totalScore += likeness * int(AllUsers[x].GetReadBooks()[y])
			totalPercentage += likeness

		if int(userBooks[y]) != BookStatus.BOOK_NOT_READ.value:
			continue

		# If there is not enough people with high enough likeness who scored the book, we just set it's score to 0.
		# 0 is for unknown recommendability.
		if totalPercentage == 0 or totalPercentage < 100:
			recommendedBooks.append(Book(AllBooks[y].GetName(), 0))
			continue

		bookScore = totalScore/totalPercentage
		book = Book(AllBooks[y].GetName(), bookScore )
		recommendedBooks.append(book)

	return recommendedBooks


def PrintReadAndUnreadBooks(userBooks):

	"""Prints the user's read and unread books.
	
	:param userBooks: Books the user has read.
	:type userBooks: int[]
	"""

	print("Books you haven't read:")
	for x in range(len(AllBooks)):
		if(int(userBooks[x]) == BookStatus.BOOK_NOT_READ.value):
			print(str(x + 1) + ": " + AllBooks[x].GetName())

	print("-------------------------------------------")
	print("Books you have read:")
	for x in range(len(AllBooks)):
		if int(userBooks[x]) != BookStatus.BOOK_NOT_READ.value:
			# Score has +5 because in the interface, scores are being shown from 0 to 10 while being stored in db from -5 to 5.
			print(str(x+1) + ": " + AllBooks[x].GetName() + ", Score: " + str(userBooks[x]))
	print("-------------------------------------------")


class Book:
	def __init__(self, bookName, avgScore):

		"""Sets variables of the Book.
		
		:param bookName: Name of the book.
		:type bookName: string

		:param avgScore: Average score of the book. Mainly used to list most recommendable books.
		:type avgScore: int
		"""
		self._bookName = bookName
		self._avgScore = avgScore

	def GetName(self):
		""" Returns the name of the book.

		:return: Name of the book.
		:rtype: string
		"""
		return self._bookName

	def GetAvgScore(self):
		""" Returns the average score of the book.

		:return: Average score of the book.
		:rtype: int
		"""
		return float(self._avgScore)


class User:

	def __init__(self, userName, readBooksStr = ""):
		""" Sets user name and read books if the parameter is provided.
		
		:param userName: User's name.
		:type userName: string

		:param readBooksStr: String version of ReadBooks array with a space between each score. Being Used to read from 'ratings.txt'.
		:type readBookStr: string
		"""
		self._userName = userName
		self._ReadBooks = []
		
		if readBooksStr != "":
			self.SetReadBooksFromStr(readBooksStr)

	def GetUserName(self):
		""" Returns the user name.

		:return: User name.
		:rtype: string
		"""
		return self._userName

	def SetReadBooksFromStr(self, readBooksStr):
		""" Converts string version of read books to the list '_ReadBooks'.
		
		:param readBooksStr: String version of ReadBooks array with a space between each score. Being Used to read from 'ratings.txt'.
		:type readBooksStr: string
		"""
		self._ReadBooks = readBooksStr.strip().split(" ")

	def SetReadBooks(self, userBooks):
		""" Replaces old _ReadBooks list with a new one.
		
		:param userBooks: List of the books the user read.
		:type userBooks: int[]
		"""
		self._ReadBooks = userBooks

	def GetReadBooks(self):
		""" Returns _ReadBooks list.
		
		:return: _ReadBooks list.
		:rtype: int[]
		"""
		return self._ReadBooks

	# When a new user is created, this function will be called.
	# Class doesn't know how many books in the list so the function needs to be called from outside the class.
	def SetReadNoBooks(self, bookAmount):
		""" Fill _ReadBooks array with 0's (BookStatus.BOOK_NOT_READ). So that the user will have no book in their list.
		:param bookAmount: Book amount in AllBooks list.
		:type bookAmount: int
		"""
		for x in range(bookAmount):
			self._ReadBooks.append(str(BookStatus.BOOK_NOT_READ.value))
			


class BookStatus(Enum):
	BOOK_NOT_READ = 0


if __name__  == "__main__": StartProgram()



