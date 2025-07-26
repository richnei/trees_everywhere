from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Account, Tree, PlantedTree

class TreeViewsTestCase(TestCase):
    def setUp(self):
        # Create users
        self.alice = User.objects.create_user(username='alice', password='1234')
        self.bob = User.objects.create_user(username='bob', password='1234')
        self.carol = User.objects.create_user(username='carol', password='1234')

        # Create accounts
        self.account_a = Account.objects.create(name='Account A')
        self.account_b = Account.objects.create(name='Account B')

        # Associate users to accounts
        self.account_a.users.set([self.alice, self.bob])
        self.account_b.users.set([self.bob, self.carol])

        # Create trees
        self.tree_alice = Tree.objects.create(name='Yellow Ipe', scientific_name='Handroanthus albus')
        self.tree_bob = Tree.objects.create(name='Araucaria', scientific_name='Araucaria angustifolia')
        self.tree_carol = Tree.objects.create(name='Jatoba', scientific_name='Hymenaea courbaril')

        # Each user plants a tree
        self.planted_alice = PlantedTree.objects.create(
            user=self.alice, tree=self.tree_alice, account=self.account_a,
            age=2, location_lat=-27.59, location_lon=-48.54
        )
        self.planted_bob = PlantedTree.objects.create(
            user=self.bob, tree=self.tree_bob, account=self.account_a,
            age=3, location_lat=-27.60, location_lon=-48.55
        )
        self.planted_carol = PlantedTree.objects.create(
            user=self.carol, tree=self.tree_carol, account=self.account_b,
            age=1, location_lat=-27.61, location_lon=-48.56
        )

        # Authenticate client as Alice
        self.client = Client()
        self.client.login(username='alice', password='1234')

    def test_user_tree_list_renders_only_user_trees(self):
        response = self.client.get(reverse('user_trees'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yellow Ipe')
        self.assertNotContains(response, 'Araucaria')
        self.assertNotContains(response, 'Jatoba')

    def test_user_cannot_access_tree_of_another_user(self):
        url = reverse('tree_detail', args=[self.planted_bob.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "You do not have permission to access this tree.", status_code=403)

    def test_account_trees_list_shows_all_trees_in_user_accounts(self):
        response = self.client.get(reverse('account_trees'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yellow Ipe')  # Alice
        self.assertContains(response, 'Araucaria')   # Bob
        self.assertNotContains(response, 'Jatoba')   # Carol

    def test_plant_tree_creates_plantedtree(self):
        tree = Tree.objects.create(name='Cashew Tree', scientific_name='Anacardium occidentale')
        location = (-27.70, -48.60)

        planted = self.alice.plant_tree(
            tree=tree,
            location=location,
            account=self.account_a,
            age=4
        )

        self.assertIsNotNone(planted.id)
        self.assertEqual(planted.user, self.alice)
        self.assertEqual(planted.tree, tree)
        self.assertEqual(float(planted.location_lat), location[0])
        self.assertEqual(float(planted.location_lon), location[1])

    def test_plant_trees_creates_multiple_plantedtrees(self):
        tree1 = Tree.objects.create(name='Brazilwood', scientific_name='Paubrasilia echinata')
        tree2 = Tree.objects.create(name='Mango Tree', scientific_name='Mangifera indica')

        locations = [
            (tree1, -27.80, -48.70, self.account_a, 2),
            (tree2, -27.81, -48.71, self.account_a, 3)
        ]

        results = self.alice.plant_trees(locations)

        self.assertEqual(len(results), 2)
        self.assertTrue(all(p.user == self.alice for p in results))
