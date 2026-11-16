typedef unsigned int uint;
struct Student
{
  int age;
  float marks;
};
union Data
{
  int number;
  float decimal;
};
enum Status
{
  ACTIVE,
  INACTIVE
};
int main()
{
  char letter = 'A';
  short int small = 10;
  long int large = 1000;
  unsigned int count = 20;
  float temperature = 36.5;
  double distance = 123.456;
  int *ptr;
  int **double_ptr;
  int numbers[10];
  int matrix[40][3];
  struct Student student;
  union Data data;
  enum Status status;
  return 0;
}

