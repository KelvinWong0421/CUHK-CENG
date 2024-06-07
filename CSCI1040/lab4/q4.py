class Pagination():

    def __init__(self, item, page_size = 10):
        self.item = item
        self.page_size = page_size

        self.total_pages = int((len(list(item))-1)/page_size)
        self.current_page = 0

    
    def get_visible_items(self):
        return self.item[self.current_page:self.current_page+self.page_size]

    def prev_page(self): 
        self.current_page -= self.page_size
        
        return self
    
    def next_page(self):
        self.current_page += self.page_size
        
        return self
    
    def first_page(self):
        self.current_page = 0
        
        return self

    def last_page(self):
        self.current_page = (self.total_pages*self.page_size)
        
        return self

    def go_to_page(self, page: int):
        if page > self.total_pages:
            self.last_page()
        elif page <= 0 :
            self.first_page()
        else:    
            self.current_page = (page*self.page_size)-self.page_size
        
        return self

alphanums = [6, 7, 12, 'a', 0, 'b', 'c', 'x', 88, 99]
page = Pagination(alphanums, 3)
print(page.get_visible_items()) # [6, 7, 12]
page.next_page()
print(page.get_visible_items()) # ['a', 0, 'b']
page.next_page().next_page()
print(page.get_visible_items()) # [99]
page.last_page().prev_page()
print(page.get_visible_items()) # ['c', 'x', 88]
page.first_page().next_page().next_page()
print(page.get_visible_items()) # ['c', 'x', 88]
page.go_to_page(-1).next_page()
print(page.get_visible_items()) # ['a', 0, 'b']

        
        
